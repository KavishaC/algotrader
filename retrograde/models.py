from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import json, time, requests, html, threading
import yfinance as yf
import pandas as pd
import numpy as np
from openai import OpenAI
from forex_python.converter import CurrencyRates
from .utils import exchange_rates
from . import config as cf
from . import benchmarks_beta as benchmarks_beta
from .test_functions.read_stock_prices import get_price, get_price_chart
from .test_functions.financial_performance import generate_performance_data
from .test_functions.asset_charts import get_candlestick_data
from decimal import Decimal
import copy

class User(AbstractUser):
    timezone = models.CharField(max_length=50, default='UTC')

    @property
    def active_portfolios(self):
        return Portfolio.filter(owner = self, archived = False)
    
    def add_portfolio(self, portfolio):
        # copied_portfolios = Portfolio()
        # pk = copied_portfolios.pk()
        copied_portfolios = copy.deepcopy(portfolio)
        copied_portfolios.owner = self
        copied_portfolios.pk = None
        copied_portfolios.archived = False
        copied_portfolios.save()
    
"""
Creates a portfolio in an unique spacetime.
"""
class Portfolio(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey("User", on_delete=models.PROTECT, related_name="portfolios")
    date = models.DateField()
    initial_capital = models.DecimalField(max_digits=12, decimal_places=0, blank=False, default=0) # define the max length of an asset
    data = models.JSONField(default=dict, blank=True)
    advice = models.CharField(max_length=1000, blank=True, null=True)
    current_data = models.JSONField(default=dict, blank=True)
    news = models.JSONField(default=dict, blank=True, null=True)
    archived = models.BooleanField(default=False)
    #TODO time_scale =  DAY,WEEK, MONTH, YEAR
    #TODO:AutoPilot #strategy = models.ForeignKey("Strategy", on_delete=models.PROTECT)

    def __str__(self):
        if self.archived:
            return f"{self.pk}. {self.owner}:\t {self.name} (Archived)"
        else:
            return f"{self.pk}. {self.owner}:\t {self.name}"

    def save(self, *args, **kwargs):
        if (not self.pk) and self.data == {}:
            # For new portfolios
            self.data = {"records": [{
                "date": self.date.isoformat(),
                "value": float(self.initial_capital),
                "cash": float(self.initial_capital),
                "assets": []
            }]}

            # Initialise price_data
            self.current_data['price_data'] = { 'date': [], 'value': [], 'cash': []}
            self.current_data['assets'] = [{
                    'index': "0",
                    'ticker': "Cash Balance",
                    'quote_type': "Cash",
                    'currency': 'USD',
                    'current_value': "{:.2f}".format(self.initial_capital),
                    'current_value_percent': "100%"
            }]

            self.news = None
        super().save(*args, **kwargs)

    def archive(self):
        self.archived = True
        self.save()

    def unarchive(self):
        self.archived = False
        self.save()

    """
    Gets current portfolio value
    """
    @property
    def value(self):
        records = self.data["records"]
        return "{:.2f}".format(records[-1]["value"])
    
    """
    Gets current cash balance value
    """
    @property
    def cash_balance(self):
        records = self.data["records"]
        return "{:.2f}".format(records[-1]["cash"])

    """
    Gets daily change in portfolio value
    """
    @property
    def change(self):
        records = self.data["records"]
        today = records[-1]["value"]
        try:
            yesterday = records[-2]["value"]
            change_percent = ((today-yesterday)/yesterday) * 100
        except:
            change_percent = 0
        change_percent_str = "{:.2f}".format(change_percent)
        if (change_percent > 0 and change_percent_str != "0.00"):
            change_percent_str = "+" + change_percent_str
        if (change_percent_str == "-0.00"):
            change_percent_str = change_percent_str[1:]
        return change_percent_str + "%"
    
    """
    Gets daily portfolio value change status
    """
    @property
    def change_status(self):
        return percentage_change_status(self.change)
    
    @property
    def profit(self):
        return "{:.2f}".format(Decimal(self.data["records"][-1]["value"]) - self.initial_capital)

    """
    Gets price data
    """
    @property
    def price_data(self):
        return json.dumps(Portfolio.objects.get(pk=self.id).current_data["price_data"])

    """
    Get asset data
    """
    @property
    def asset_data(self):
        return Portfolio.objects.get(pk=self.id).current_data["assets"]

    """
    Tick forward the portfolio date
    """
    def tick(self, tick_timedelta_str):
        start_time = time.time()
        ticker_histories = {}

        if internet_disconnected(): return

        self.update_datetime(tick_timedelta_str)
        update = self.write_missing_records(ticker_histories)
        self.update_asset_data(update, ticker_histories)
        self.generate_price_data()
        self.sort_asset_data()

        # Clear advice and news
        self.clear_advice()
        self.news = None

        self.save()

        print_timing("total tick", start_time)
        return
    
    """
    Update datetime of portfolio 
    """
    def update_datetime(self, tick_timedelta_str):
        dt = self.date
        
        if (tick_timedelta_str == "1d"):
            dt += timedelta(days=1)
        elif (tick_timedelta_str == "1wk"):
            dt += timedelta(days=(7 - dt.weekday()))
        elif (tick_timedelta_str == "1mo"):
            dt += relativedelta(months=1)
            dt.replace(day=1)
        elif (tick_timedelta_str == "3mo"):
            # TODO
            tick_timedelta = timedelta(hours=1)
        elif (tick_timedelta_str == "6mo"):
            # TODO
            tick_timedelta = timedelta(hours=1)
        elif (tick_timedelta_str == "1y"):
            # TODO
            tick_timedelta = timedelta(hours=1)
        
        self.date = dt
        self.save()

    """
    Write missing records upto current date of portfolio
    """        
    def write_missing_records(self, ticker_histories):
        start_time = time.time()
        update = False
        last_record = self.data["records"][-1]
        record_date = datetime.fromisoformat(last_record["date"]).date()
        portfolio_date = self.date

        # Write missing records
        while (record_date < portfolio_date):
            #print("reading last_record[datetime]: ", record_date, "not yet at current_time :", portfolio_date)
            update = True
            convert = False

            # Generate record for next day
            record_date += timedelta(days=1)
            next_record = {
                "date": record_date.isoformat(),
                "cash": last_record["cash"],
                "assets": []
            }

            # Manage threads
            price_threads = []
            start_time = time.time()
            for asset in last_record["assets"]:
                ticker = asset["ticker"]

                # Get history of asset
                if ticker not in ticker_histories:
                    thread = threading.Thread(target=get_ticker_history, args=(ticker, record_date, portfolio_date, ticker_histories))
                    price_threads.append(thread)
                    thread.start()
                
                # Get history of benchmark.
                benchmark = self.get_benchmark(asset)
                if benchmark not in ticker_histories:
                    thread = threading.Thread(target=get_ticker_history, args=(benchmark, record_date, portfolio_date, ticker_histories))
                    price_threads.append(thread)
                    thread.start()
            
            # Join threads
            for thread in price_threads:
                thread.join()

            start_time = time.time()

            # Write asset data for next day
            write_threads = []
            value = next_record["cash"]
            for asset in last_record["assets"]:
                ticker = asset["ticker"]
                daily_data = ticker_histories[ticker]
                thread = threading.Thread(target=write_asset_record, args=(record_date, daily_data, ticker, asset, next_record))
                write_threads.append(thread)
                thread.start()

            # Join threads
            for thread in write_threads:
                thread.join()

            for asset_record in next_record["assets"]:
                value += asset_record["value"]

            next_record['assets'] = [item for item in next_record['assets'] if item['units'] != 0]

            # Update rest of portfolio record
            next_record["value"] = value
            self.data["records"].append(next_record)
            last_record = next_record

        self.save()
        print_timing("write_missing_records", start_time)
        return update    

    """
    Update asset data to match the latest record
    """                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
    def update_asset_data(self, update, ticker_histories):
        if update:
            last_record = self.data["records"][-1]
            record_date = datetime.fromisoformat(last_record["date"]).date()

            # Update asset_data
            for asset in last_record["assets"]:

                ticker = asset['ticker']
                history = ticker_histories[ticker]
                for asset_record in self.current_data["assets"]:
                    if asset_record['ticker'] == ticker:
                        yesterday_price = get_price(record_date - timedelta(days=1), history)
                        current_price_change = percentage_change(asset['price'], yesterday_price)
                        asset_record['current_price'] = "{:.2f}".format(asset['price'])
                        asset_record['current_price_change'] = current_price_change
                        asset_record['current_price_change_status'] = percentage_change_status(current_price_change)
                        asset_record['current_num_units'] = asset['units']
                        asset_record['current_value'] = "{:.2f}".format(asset['value'])
                        asset_record['current_value_percent'] = "{:.2f}".format(asset['value'] * 100 / last_record['value']) + "%"
                        asset_record['price_chart'] = get_price_chart(history, self.date)

                        if "rate" in asset:
                            asset_record['current_price_usd'] = asset["rate"] * asset['price']
                        asset_record['beta_chart'] = self.get_beta_chart_data(asset, ticker_histories),

            # save to file
            if cf.SAVE_TO_FILE:
                f = "server_portfolio_records_" + str(self.id) + ".json"

                start_time = time.time()
                with open("saved_files/" + f, "w") as json_file:
                    json.dump({"records": self.data["records"]}, json_file, indent=2)
        self.save()

    """
    Clear advice and news
    """
    def clear_advice(self):
        if cf.GENERATE_ADVICE:
            self.advice = None

    """
    Generate value data for chart using records
    """
    def generate_price_data(self):
        self.current_data['price_data'] = { 'date': [], 'value': [], 'cash': []}
        records = Portfolio.objects.get(pk=self.id).data["records"]

        assets = []

        # Create charts for all assets owned so far
        for record in records:
            for asset_record in record['assets']:
                if asset_record['ticker'] not in assets:
                    assets.append(asset_record["ticker"])
                    self.current_data['price_data'][asset_record["ticker"]] = []

        # Update data for each record
        for record in self.data["records"]:
            self.current_data['price_data']['date'].append(record["date"])
            self.current_data['price_data']['cash'].append(record["cash"])
            self.current_data['price_data']['value'].append(record["value"])
            
            # Update data for each asset
            for asset in assets:
                value = None
                for asset_record in record["assets"]:
                    if asset_record["ticker"] == asset:
                        value = asset_record["value"]
                self.current_data['price_data'][asset].append(value)

        self.current_data['price_data'] = self.current_data['price_data']
        self.save()
        return
    
    """
    Sorts and indexes asset data
    """
    def sort_asset_data(self):
        asset_data = Portfolio.objects.get(pk=self.id).current_data["assets"]

        asset_data[:] = [item for item in asset_data if not item["ticker"] == "Cash Balance"]

        # Remove asset records with no units
        asset_data = [asset_record for asset_record in asset_data if asset_record['current_num_units'] != "0"]
        
        asset_data = sorted(asset_data, key=lambda x: float(x['current_value']), reverse=True)
        
        i = 0
        for asset in asset_data:
            asset['index'] = str(i)
            i += 1

        last_record = Portfolio.objects.get(pk=self.id).data['records'][-1]
        cash_balance = last_record['cash']
        value = last_record['value']

        asset_data.append({
                'index': str(i),
                'ticker': "Cash Balance",
                'quote_type': "Cash",
                'currency': 'USD',
                'current_value': "{:.2f}".format(cash_balance),
                'current_value_percent': "{:.2f}".format(cash_balance * 100 / value) + "%"
        })

        self.current_data["assets"] = asset_data
        self.save()
        return
    
    def get_advice(self):
        # save changes to database
        if (self.advice == None):
            if cf.GENERATE_ADVICE:
                self.generate_advice()
            else:
                return {"advice": "Advice Generation turned off."}
        return {"advice": self.advice}

    """
    Generate advice for the portfolio
    """
    def generate_advice(self):
        if internet_disconnected(): return
        
        client = OpenAI(api_key=cf.OPENAI_API)

        start = cf.ADVICE_PROMPT
        
        start += " Limit your response to " + str(cf.ADVICE_WORD_LIMIT) + " words.\n" 
        
        last_record = Portfolio.objects.get(pk=self.id).data["records"][-1]
        request = start + str(last_record)

        # Make OpenAI call
        start_time = time.time()
        chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": request,
            }],
            model=cf.CHATGPT_VERSION,
        )
        print("API_TIMING: OpenAI call took", str(round(time.time() - start_time, 2)) + "s")

        #print("AI response object:", chat_completion)
        first_choice = chat_completion.choices[0]
        content = first_choice.message.content
        content = html.escape(content)
        #print("Response:", content)
        with open("saved_files/" + 'AI_feedback.txt', 'a') as file:
            # Add text to the file
            file.write("Date: " + str(datetime.now()) + '\n')
            file.write("Q: " + start + '\n')
            file.write("A: " + content + '\n\n\n')

        self.advice = content.replace("\n", "").replace("EOF", "")
        self.save()
        
    def get_news(self):
        if (self.news == None):
            self.generate_news()
        return {"news": self.news}
    
    """
    Generate news for the portfolio
    """
    def generate_news(self):
        if internet_disconnected(): return

        url = 'https://www.alphavantage.co/query?'

        # Tinker the parameters later to get optimal result
        parameters = {
            "function": "NEWS_SENTIMENT",
            #"tickers": "AAPL",
            #"topics": "financial_markets,finance,ipo",
            "sort": "RELEVANCE",
            "apikey": cf.ALPHAVANTAGE_API,
            "time_from": self.date.strftime("%Y%m%d") + "T0000",
            "time_to": self.date.strftime("%Y%m%d") + "T2359",
            "limit": str(cf.NEWS_ITEM_LIMIT),
        }

        index = 0
        for parameter in parameters:
            if index != 0:
                url += '&'

            url += parameter
            url += '='
            url += parameters[parameter]
            index += 1

        start_time = time.time()
        r = requests.get(url)
        print("API_TIMING: alpha vantage call took", str(round(time.time() - start_time, 2)) + "s:")

        data = r.json()

        #print(data)
        if 'feed' in data:
            # Format dates
            for article in data['feed']:
                d = datetime.strptime(article["time_published"], "%Y%m%dT%H%M%S")
                article["time_published"] = d.strftime("%I:%M %p, %B %d, %Y").replace(" 0", " ")
                article["title"] = article["title"].replace("( ", "(").replace(" )", ")")

                if article["time_published"].startswith("0"):
                    article["time_published"] = article["time_published"][1:]

            f = "alpha_news_" + "1" + ".json"

            with open("saved_files/" + f, "w") as json_file:
                json.dump({"data": data}, json_file, indent=2)
        else:
            # manage other errors
            print("ERROR:", data)
            data = None
        self.news = data
        self.save()
    
    """
    Execute a buy trade order
    """
    def buy(self, ticker, num_units):
        if internet_disconnected(): return
        price = None
        existing_asset = False
        convert = False

        if num_units != int(num_units):
            num_units = round(num_units, 2)
        else:
            num_units = int(num_units)

        print("buy:", ticker, "num_units:", num_units)

        if num_units == 0:
            print("Unsuccessful: provide num_units as a multiple of 0.01")
            return

        # Remove last record
        last_record = self.data["records"].pop()

        #print("last_record", last_record)

        # Look if the asset already exists in portfolio
        for asset in last_record['assets']:
            if asset['ticker'] == ticker:
                print("asset is an existing asset")
                existing_asset = True
                price = asset['price']
                if ('currency' in asset):
                    convert = True
                    from_currency = asset['currency']
                    rate = asset['rate']

        # If new asset get price data from yfinance
        if existing_asset == False:
            ticker_object = yf.Ticker(ticker)

            # Call yfinance to get history data for the past 15 days 
            try:
                start_time = time.time()
                history = ticker_object.history(start=self.date - relativedelta(months=3), end=self.date + timedelta(days=1), interval='1d')
                print("API_TIMING: yfinance call for", ticker, "took", str(round(time.time() - start_time, 2)) + "s")
                daily_data = history['Close']
            except:
                exit("yfinance request failed. Abort")


            start_time = time.time()
            info = ticker_object.info
            print("API_TIMING: yfinance info call for", ticker, "took", str(round(time.time() - start_time, 2)) + "s")

            price = get_price(self.date, daily_data)
            price_chart = get_price_chart(daily_data, self.date)
            # Read currency of asset
            if 'currency' in ticker_object.info:
                from_currency = ticker_object.info['currency']
                print("from_currency", from_currency)
                if from_currency != "USD":
                    convert = True

        purchase_value = num_units * price

        # If non-USD asset convert purchase_value
        if convert:
            if not existing_asset:
                rate = exchange_rates.get_exchange_rate(from_currency, self.date)

            purchase_value *= rate

        #print("purchase value = price * num_units = ", price, num_units, "=", purchase_value, "<", 'cash_balance', last_record["cash"])
        
        # Verify adequate cash balance
        if last_record["cash"] < purchase_value:
            print("Cash balance not adequate for transaction")
            return

        # Deduct cash balance
        last_record['cash'] -= purchase_value

        # Update records
        if existing_asset:
            # Update existing record
            for asset in last_record['assets']:
                if asset['ticker'] == ticker:
                    new_num_units = asset['units'] + num_units
                    if new_num_units == int(new_num_units):
                        new_num_units = int(new_num_units)
                        new_num_units_str = str(new_num_units)
                    else:
                        new_num_units = round(new_num_units, 2)
                        new_num_units_str ="{:.2f}".format(new_num_units, 2)

                    print("new_num_units:", new_num_units)
                    asset['units'] = new_num_units
                    new_value = asset['value'] + purchase_value
                    asset['value'] = new_value
            
            # Update asset record
            for asset in self.current_data["assets"]:
                if asset['ticker'] == ticker:
                    print("new_num_units:", new_num_units)
                    asset['current_num_units'] = new_num_units_str
                    asset['current_value'] = "{:.2f}".format(round(new_value, 2))
                    asset['current_value_percent'] = "{:.2f}".format(round(new_value * 100 / last_record['value'], 2)) + "%"
                    
        else:
            new_num_units = num_units
            if new_num_units == int(new_num_units):
                new_num_units = int(new_num_units)
                new_num_units_str = str(new_num_units)
            else:
                new_num_units = round(new_num_units, 2)
                new_num_units_str ="{:.2f}".format(new_num_units, 2)
            # Add new record
            asset = {
                "price": price,
                "units": num_units,
                "value": purchase_value,
                "ticker": ticker
            }
            if convert:
                asset['currency'] = from_currency
                asset['rate'] = rate
            last_record['assets'].append(asset)

            # Add new asset to asset data

            long_name = info.get('longName', '')
            if (ticker=="GC=F"):
                long_name = "Gold"

            current_price_change = percentage_change(get_price(self.date, daily_data), get_price(self.date - timedelta(days=1), daily_data))
            
            current_data_record = {
                'ticker': ticker,
                'country': info.get('country', ''),
                'quote_type': info.get('quoteType', ''),
                'currency': info.get('currency', ''),
                'exchange': info.get('exchange', ''),
                'long_business_summary': info.get('longBusinessSummary', ''),
                'long_name': long_name,
                'current_price': "{:.2f}".format(round(price, 2)),
                'current_price_change': current_price_change,
                'current_price_change_status': percentage_change_status(current_price_change),
                'current_num_units': new_num_units_str,
                'current_value': "{:.2f}".format(round(purchase_value, 2)),
                'current_value_percent': "{:.2f}".format(round(purchase_value * 100 / last_record['value'], 2)) + "%",
                'price_chart': price_chart,
                'beta_chart': [self.get_beta_chart_data(asset, {ticker: daily_data})],
            }

            if convert:
                current_data_record["current_price_usd"] = rate * price
            self.current_data["assets"].append(current_data_record)

        # Add updated record
        self.data["records"].append(last_record)
        self.save()
        self.sort_asset_data()

        self.clear_advice()

        # Save to file
        if cf.SAVE_TO_FILE:
            f = "server_portfolio_records_" + str(self.id) + ".json"
            start_time = time.time()
            with open("saved_files/" + f, "w") as json_file:
                json.dump({"records": self.data["records"]}, json_file, indent=2)
            print("TIMING: saving to file for", ticker, "took", str(round(time.time() - start_time, 2)) + "s")
        self.save()

        print("successful buy")
        return
    
    """
    Execute a sell trade order
    """
    def sell(self, ticker, num_units):
        if internet_disconnected(): return
        existing_asset = False
        
        # Remove last record
        last_record = self.data["records"].pop()

        if num_units != int(num_units):
            num_units = round(num_units, 2)
        else:
            num_units = int(num_units)

        if num_units == 0:
            print("Unsuccessful: provide num_units as a multiple of 0.01")
            return
        
        print("sell:", ticker, "num_units:", num_units)

        # Look for asset
        for asset in last_record['assets']:
            if asset['ticker'] == ticker:
                existing_asset = True
                price = asset['price']
                units = asset['units']

                # Verify adequacy of units
                if units < num_units:
                    print("Not enough units. Cannot complete transaction")
                    return
                
                asset['units'] = round(asset['units'] - num_units, 2)
                purchase_value = price * num_units

                # For non-USD assets
                if "currency" in asset:
                    from_currency = asset["currency"]
                    rate = exchange_rates.get_exchange_rate(from_currency, self.date)
                    purchase_value *= rate

                asset['value'] -= purchase_value
                last_record["cash"] += purchase_value
                new_num_units = asset['units']
                if new_num_units == int(new_num_units):
                    new_num_units = int(new_num_units)
                    new_num_units_str = str(new_num_units)
                else:
                    new_num_units = round(new_num_units, 2)
                    new_num_units_str ="{:.2f}".format(new_num_units, 2)

                # Update asset record
                for asset_record in self.current_data["assets"]:
                    if asset_record['ticker'] == ticker:
                        print("new_num_units:", new_num_units_str)
                        asset_record['current_num_units'] = new_num_units_str
                        asset_record['current_value'] = "{:.2f}".format(asset['value'])
                        asset_record['current_value_percent'] = "{:.2f}".format(asset['value'] * 100 / last_record['value']) + "%"

        # Exit if asset does not exist
        if existing_asset == False:
            print("Do not own asset. Cannot complete transaction")
            return
        
        # Remove asset records with no units
        last_record['assets'] = [item for item in last_record['assets'] if item['units'] != 0]

        # Update data
        self.data["records"].append(last_record)
        self.save()
        self.sort_asset_data()

        self.clear_advice()
    
        print("successful")

        # Save to file
        f = "server_portfolio_records_" + str(self.id) + ".json"

        if cf.SAVE_TO_FILE:
            start_time = time.time()
            with open("saved_files/" + f, "w") as json_file:
                json.dump({"records": self.data["records"]}, json_file, indent=2)
            print("TIMING: saving to file for", ticker, "took", str(round(time.time() - start_time, 2)) + "s")

        print("Successful")
        return

    @property
    def financial_performance(self):
        return generate_performance_data(self.data["records"])

    """
    Search for the data of an asset
    """
    def search_asset(self, ticker):
        if internet_disconnected(): return
        
        # Capitalize
        ticker = ticker.upper()

        ticker_object = yf.Ticker(ticker)

        # Call yfinance to get history data for the past 30 days 
        try:
            start_time = time.time()
            history = ticker_object.history(start=self.date - relativedelta(months=3), end=self.date + timedelta(days=1), interval='1d')
            print("API_TIMING: yfinance call for", ticker, "took", str(round(time.time() - start_time, 2)) + "s")

        except:
            print("search failed: yfinance request failed.")
            return
        
        # Check if search succeeded
        if history.empty:
            return {
                "ERROR": "Unable to retrieve asset data!"
            }

        daily_data = history['Close']
        
        start_time = time.time()
        info = ticker_object.info
        print("API_TIMING: yfinance info call for", ticker, "took", str(round(time.time() - start_time, 2)) + "s")

        price = get_price(self.date, daily_data)
        price_chart = get_price_chart(daily_data, self.date)

        convert = False
        # Read currency of asset
        if 'currency' in ticker_object.info:
            from_currency = ticker_object.info['currency']
            if from_currency != "USD":
                convert = True

        dollar_value = price

        # If non-USD asset convert purchase_value
        if convert:
            rate = exchange_rates.get_exchange_rate(from_currency, self.date)

            dollar_value *= rate

        current_price_change = percentage_change(get_price(self.date, daily_data), get_price(self.date - timedelta(days=1), daily_data))
        
        return {
            'ticker': ticker,
            'country': info.get('country', ''),
            'quote_type': info.get('quoteType', ''),
            'currency': info.get('currency', ''),
            'exchange': info.get('exchange', ''),
            'long_business_summary': info.get('longBusinessSummary', ''),
            'long_name': info.get('longName', ''),
            'current_price': "{:.2f}".format(round(price, 2)),
            'current_price_change': current_price_change,
            'current_price_change_status': percentage_change_status(current_price_change),
            'price_chart': price_chart,
            'current_price_usd': dollar_value,
            'beta_chart': [self.get_beta_chart_data({"ticker": ticker, "currency": info.get('currency', '')}, {ticker: daily_data})],
        }
    
    def get_benchmark(self, asset):
        if "currency" in asset:
            currency = asset["currency"]
        else:
            currency = "USD"
        benchmarks = benchmarks_beta.benchmarks

        try:
            benchmark_ticker = benchmarks[currency]
        except:
            #print("benchmark for", currency, "not available. Unable to generate beta charts")
            benchmark_ticker = benchmarks["USD"]
        return benchmark_ticker

    def get_beta_chart_data(self, asset_record, ticker_histories):
        ticker = asset_record["ticker"]
        benchmark = self.get_benchmark(asset_record)
        asset_data = ticker_histories[ticker]
        try:
            benchmark_data = ticker_histories[benchmark]
        except:
            get_ticker_history(benchmark, self.date, self.date, ticker_histories)
            benchmark_data = ticker_histories[benchmark]

        #print("benchmark for", ticker, "is", benchmark)
        
        # Combine data into a DataFrame
        data = pd.concat([asset_data, benchmark_data], axis=1)
        data.columns = ['Asset', 'Benchmark']

        #print("data", data)

        # Calculate daily returns
        returns = data.pct_change().dropna() * 100
        returns = returns[returns.index <= self.date]
        #print("returns", returns)

        # Calculate beta using linear regression
        asset_returns = returns['Asset'].values
        benchmark_returns = returns['Benchmark'].values

        coefficients = np.polyfit(benchmark_returns, asset_returns, 1)
        beta, alpha = coefficients

        # Create scatter plot with regression line
        scatter_plot_data = [{'x': benchmark_returns[i], 'y': asset_returns[i]} for i in range(len(benchmark_returns))]
        x_low = benchmark_returns.min()
        x_high = benchmark_returns.max()
        line_plot_data = [{'x': x_low, 'y': beta * x_low + alpha}, {'x': x_high, 'y': beta * x_high + alpha}]
        
        beta = {
            "line_plot_data": line_plot_data,
            "scatter_plot_data": scatter_plot_data,
            "beta": "{:.2f}".format(round(beta, 2)),
            "benchmark": benchmark,
        }
        return beta
    
"""
Percentage change value2 => value1
"""
def percentage_change(value1, value2):
    change_percent = ((value1-value2)/value2) * 100
    change_percent_str = "{:.2f}".format(round(change_percent, 2))
    if (change_percent > 0):
        change_percent_str = "+" + change_percent_str
    return change_percent_str + "%"

def percentage_change_status(str):
    if (str.startswith("+")):
        return "POSITIVE"
    elif (str.startswith("-")):
        return "NEGATIVE"
    else:
        return "ZERO"

def internet_disconnected():
    start_time = time.time()
    try:
        requests.get("https://www.google.com", timeout=5)
        disconnected = False
    except requests.ConnectionError:
        print_timing("internet check", start_time)
        print("ERROR: Cannot tick. Not connected to the internet.")
        disconnected = True
    return disconnected
    
def get_ticker_history(ticker, record_date, portfolio_date, ticker_histories):

    # check if ticker cache has data
    #print(type(record_date))
    #print(type(portfolio_date))

    date = min(record_date, portfolio_date)

    start_time = time.time()
    #print(type(date))
    """
    print("CACHE LOOKUP: ticker=", ticker, ", date=", date)
    
    
    try:
        daily_data = TickerData.objects.get(ticker = ticker, date = date).get_daily_data()

    except TickerData.DoesNotExist:
        try:
            daily_data = yf.Ticker(ticker).history(start=date - relativedelta(months=3), end=portfolio_date + timedelta(days=2), interval='1d')['Close']
            print("API_TIMING: yfinance call for", ticker, "took", str(round(time.time() - start_time, 2)) + "s")
            
        except:
            exit("yfinance request failed. Abort")
        
        try:
            daily_data.index = daily_data.index.date
        except:
            pass

        # Save ticker data to cache
        new_ticker_data = TickerData.objects.create(ticker=ticker, date=date)
        new_ticker_data.set_daily_data(daily_data)

        print("new ticker data object saved. TickerData.object now is")

        # Print All
        # Retrieve all StockData objects
        all_ticker_data = TickerData.objects.all()

        # Iterate and print each object
        for ticker_data in all_ticker_data:
            print(ticker_data)
            #print(ticker_data.get_daily_data())
    """

    try:
        daily_data = yf.Ticker(ticker).history(start=date - relativedelta(months=3), end=portfolio_date + timedelta(days=2), interval='1d')['Close']
        print("API_TIMING: yfinance call for", ticker, "took", str(round(time.time() - start_time, 2)) + "s")
        
    except:
        exit("yfinance request failed. Abort")
    
    try:
        daily_data.index = daily_data.index.date
    except:
        pass

    print("added ticker_history for ticker=", ticker, ", date=", date)

    ticker_histories[ticker] = daily_data

    return 

def write_asset_record(record_date, daily_data, ticker, asset, next_record):
    # Create asset record
    current_price = get_price(record_date, daily_data)
    new_asset_record = {
        "ticker": ticker,
        "units": asset["units"],
        "price": current_price,
        "value": asset["units"] * current_price
    }
    if ('currency' in asset):
        convert = True
        new_asset_record["currency"] = asset['currency']
        from_currency = asset['currency']

        rate = exchange_rates.get_exchange_rate(from_currency, record_date)

        new_asset_record["rate"] = rate
        amount = asset["units"] * current_price * rate
        new_asset_record["value"] = amount

    else:
        new_asset_record["value"] = asset["units"] * current_price

    next_record["assets"].append(new_asset_record)

def print_timing(task, start_time):
    if cf.PRINT_TIMING == True:
        print(f"TIMING: update {task:<30} = {round(time.time() - start_time, 2)}s")

def custom_print(*args, **kwargs):
    # Get the current time
    current_time = time.strftime("%Y-%m-%d %I:%M:%S %p")

    # Print the current time
    print(f"[{current_time}]", end=" ")

    # Print the provided message using the same arguments as print()
    print(*args, **kwargs)

class TickerData(models.Model):
    ticker = models.CharField(max_length=50)
    date = models.DateField()
    daily_data_json = models.JSONField(null=True)

    class Meta:
        unique_together = ('ticker', 'date')

    def set_daily_data(self, daily_data):
        self.daily_data_json = daily_data.to_json(orient='split')

    def get_daily_data(self):
        return pd.read_json(self.daily_data_json, orient='split')
    
    def __str__(self):
            return f"{self.ticker} on {self.date}"