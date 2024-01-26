from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import json, time, requests, html
import yfinance as yf
import pandas as pd
from openai import OpenAI
from forex_python.converter import CurrencyRates

from .test_functions.read_stock_prices import get_price, get_price_chart
from .test_functions.financial_performance import generate_performance_data
from .test_functions.asset_charts import get_candlestick_data

# Configuration
SAVE_TO_FILE = True

# Advice
GENERATE_ADVICE = True

# News
GENERATE_NEWS = True
ALPHAVANTAGE_API = "V3UO2MUD5E7I896L"
NEWS_ITEM_LIMIT = 50

# AI
CHATGPT_VERSIONS = {"3.5": "gpt-3.5-turbo", "4": "gpt-4"}
CHATGPT_VERSION = CHATGPT_VERSIONS['4']
ADVICE_PROMPT_OPTIONS = [
            "I am sending you a copy of my portfolio. Asses my current investment strategy based on global stock market on the given date. Take to account the holding of each stock given by value.",
            "Describe in 30 words the nature of the global stock market on the given date.",
            "If there is a way to improve the portfolio give feedback. If you think there is no Otherwise some fact the market trends of the asset held in the portfolio.",
            "Give me some random piece of investment advice relevant to my portfolio. Value the portion of the investment based on their values."
        ]
ADVICE_PROMPT = ADVICE_PROMPT_OPTIONS[0]
ADVICE_WORD_LIMIT = 40

class User(AbstractUser):
    timezone = models.CharField(max_length=50, default='UTC')
    #account_balance = models.DecimalField(max_digits=8, decimal_places=2)# summation of all portfolios owned by user

    @property
    def active_portfolios(self):
        return Portfolio.filter(owner = self, archived = False)
"""
Creates a portfolio in an unique spacetime. "Colombo, 13th september 2020". Smallest measure of time is a minute.
"""
class Portfolio(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey("User", on_delete=models.PROTECT, related_name="portfolios")
    date = models.DateField()
    initial_capital = models.DecimalField(max_digits=12, decimal_places=0, blank=False, default=0) # define the max length of an asset
    data = models.JSONField(default=dict, blank=True)
    advice = models.CharField(max_length=1000, blank=True)
    current_data = models.JSONField(default=dict, blank=True)
    news = models.JSONField(default=dict, blank=True)
    archived = models.BooleanField(default=False)
    #TODO time_scale =  DAY,WEEK, MONTH, YEAR
    #TODO:AutoPilot #strategy = models.ForeignKey("Strategy", on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        if not self.pk:
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
                    'current_value_percent': "100%",
                    # other data such as candlestick, price
            }]
            
            if GENERATE_NEWS:
                self.news = self.generate_news()
            else:
                self.news = {"feed": [], "items": "0"}
            super().save(*args, **kwargs)

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

        if not is_internet_connected():
            print("ERROR: Cannot tick. Not connected to the internet.")
            return

        dt = self.date
        
        # move datetime to desired position
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
        
        # update datetime
        self.date = dt

        # update each asset record so that records are available upto portfolio datetime
        self.update()

        # update price data
        self.generate_price_data()

        # sorts asset data
        self.sort_asset_data()

        # save changes to database
        if GENERATE_ADVICE:
            self.generate_advice()

        if GENERATE_NEWS:
            self.news = self.generate_news()

        self.save()
        return
    
    """
    Writes records to portfolio date
    """
    def update(self):
        print("updating records...")
        last_record = self.data["records"][-1]
        record_date = datetime.fromisoformat(last_record["date"]).date()
        portfolio_date = self.date

        ticker_histories = {}
        update = False
        #print("Writing records upto present time of portfolio")

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

            # Write asset data for next day
            value = next_record["cash"]
            for asset in last_record["assets"]:
                ticker = asset["ticker"]
                #print("updating", ticker, "for", self.date)

                if ticker not in ticker_histories:
                    #print(ticker, "not in ticker histories")
                    try:
                        # Generates history data for asset
                        start_time = time.time()
                        # redo the start time to include a minimum of 30 days
                        daily_data = yf.Ticker(ticker).history(start=min(record_date, portfolio_date) - relativedelta(months=3), end=portfolio_date + timedelta(days=2), interval='1d')['Close']
                        print("API_TIMING: yfinance call for", ticker, "took", str(round(time.time() - start_time, 3)) + "s")
                        
                    except:
                        exit("yfinance request failed. Abort")
                    
                    #print("daily_data:", daily_data)
                    #print("adding ticker history")
                    ticker_histories[ticker] = daily_data

                # create asset record
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
                    to_currency = 'USD'

                    c = CurrencyRates()

                    start_time = time.time()
                    rate = c.get_rate(from_currency, to_currency, record_date)
                    print("API_TIMING: forex_python call for", ticker, "took", str(round(time.time() - start_time, 3)) + "s")

                    print("from", from_currency, "to", to_currency)
                    print(from_currency, current_price, "=", to_currency, current_price * rate )

                    new_asset_record["rate"] = rate
                    amount = asset["units"] * current_price * rate
                    new_asset_record["value"] = amount

                else:
                    new_asset_record["value"] = asset["units"] * current_price

                value += new_asset_record["value"]
                next_record["assets"].append(new_asset_record)

            next_record['assets'] = [item for item in next_record['assets'] if item['units'] != 0]

            # update rest of portfolio record
            next_record["value"] = value
            #print("added new record:", next_record)
            self.data["records"].append(next_record)
            last_record = next_record                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
        
        #print("records (calling from update):", self.data["records"])
        
        # Save changes
        self.save()

        if update:
            # Update asset_data
            #print("histories:", ticker_histories)
            for asset in last_record["assets"]:
                ticker = asset['ticker']
                #print("looking for history of:", ticker)
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
                        # Save data as candlestick and price data
                        # ... use history to generate candlestick and price data and save to current_data
                        asset_record['price_chart'] = get_price_chart(history, self.date)
                        if "rate" in asset:
                            asset_record['current_price_usd'] = asset["rate"] * asset['price']

            # save to file
            if SAVE_TO_FILE:
                f = "server_portfolio_records_" + str(self.id) + ".json"

                start_time = time.time()
                with open("saved_files/" + f, "w") as json_file:
                    json.dump({"records": self.data["records"]}, json_file, indent=2)
                print("TIMING: saving to file took", str(round(time.time() - start_time, 3)) + "s")

        #print("done updating records...")
        return
    
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

        #print("asset data", asset_data)
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
                'current_value_percent': "{:.2f}".format(cash_balance * 100 / value) + "%",
                # other data such as candlestick, price
        })

        self.current_data["assets"] = asset_data
        self.save()
        return

    def generate_advice(self):
        if not is_internet_connected():
            print("ERROR: Cannot generate advice. Not connected to the internet.")
            return
        
        # we recommend using python-dotenv to add OPENAI_API_KEY="My API Key" to your .env file
        # so that your API Key is not stored in source control.
        client = OpenAI(api_key="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",)

        start = ADVICE_PROMPT
        
        start += " Limit your response to " + str(ADVICE_WORD_LIMIT) + " words.\n" 
        
        last_record = Portfolio.objects.get(pk=self.id).data["records"][-1]
        request = start + str(last_record)
        #print("Request:", start)

        # Make OpenAI call
        start_time = time.time()
        chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": request,
            }],
            model=CHATGPT_VERSION,
        )
        print("API_TIMING: OpenAI call took", str(round(time.time() - start_time, 3)) + "s")

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


    def generate_news(self):
        if not is_internet_connected():
            print("ERROR: Cannot generate news. Not connected to the internet.")
            return
        url = 'https://www.alphavantage.co/query?'

        # Tinker the parameters later to get optimal result
        parameters = {
            "function": "NEWS_SENTIMENT",
            #"tickers": "AAPL",
            #"topics": "financial_markets,finance,ipo",
            "sort": "RELEVANCE",
            "apikey": ALPHAVANTAGE_API,
            "time_from": self.date.strftime("%Y%m%d") + "T0000",
            "time_to": self.date.strftime("%Y%m%d") + "T2359",
            "limit": str(NEWS_ITEM_LIMIT),
        }
        #url = 'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=AAPL&apikey=demo'

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
        print("API_TIMING: alpha vantage call took", str(round(time.time() - start_time, 3)) + "s:", url)

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
            data = {"feed": [], "items": "0"}
        return data
    
    """
    Updated the most recent record. Minus cash plus units plus value plus port value
    """
    def buy(self, ticker, num_units):
        if not is_internet_connected():
            print("ERROR: Cannot buy asset. Not connected to the internet.")
            return
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
                print("API_TIMING: yfinance call for", ticker, "took", str(round(time.time() - start_time, 3)) + "s")
                daily_data = history['Close']
            except:
                exit("yfinance request failed. Abort")
            
            start_time = time.time()
            info = ticker_object.info
            print("API_TIMING: yfinance info call for", ticker, "took", str(round(time.time() - start_time, 3)) + "s")

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
                to_currency = 'USD'
                c = CurrencyRates()

                print("from", from_currency, "to", to_currency)

                # Convert using forex_python
                start_time = time.time()
                rate = c.get_rate(from_currency, to_currency, self.date)
                print("API_TIMING: forex_python call for", ticker, "took", str(round(time.time() - start_time, 3)) + "s")

                print(from_currency, price, "=", to_currency, price * rate )
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
                # other data such as candlestick, price
                'price_chart': price_chart,
            }

            if convert:
                current_data_record["current_price_usd"] = rate * price
            self.current_data["assets"].append(current_data_record)

        # Add updated record
        self.data["records"].append(last_record)
        self.save()
        self.sort_asset_data()

        # Generate advice to updated portfolio
        if GENERATE_ADVICE:
            self.generate_advice()


        # Save to file
        if SAVE_TO_FILE:
            f = "server_portfolio_records_" + str(self.id) + ".json"
            start_time = time.time()
            with open("saved_files/" + f, "w") as json_file:
                json.dump({"records": self.data["records"]}, json_file, indent=2)
            print("TIMING: saving to file for", ticker, "took", str(round(time.time() - start_time, 3)) + "s")
        self.save()

        print("successful buy")
        return

    def sell(self, ticker, num_units):
        if not is_internet_connected():
            print("ERROR: Cannot sell. Not connected to the internet.")
            return
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
                    to_currency = 'USD'
                    print("from", from_currency, "to", to_currency)

                    c = CurrencyRates()

                    # Get rate from forex_python
                    start_time = time.time()
                    rate = c.get_rate(from_currency, to_currency, self.date)
                    print("API_TIMING: forex_python call for", ticker, "took", str(round(time.time() - start_time, 3)) + "s")

                    print(from_currency, price, "=", to_currency, price * rate )
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
                
                    """                     # Reassess cash percentage
                    if asset_record['ticker'] == "Cash Balance":
                        asset_record['current_value'] = "{:.2f}".format(last_record["cash"])
                        asset_record['current_value_percent'] = "{:.2f}".format(last_record["cash"] * 100 / last_record['value']) + "%"
                    """

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

        if GENERATE_ADVICE:
            self.generate_advice()
    
        print("successful")

        # Save to file
        f = "server_portfolio_records_" + str(self.id) + ".json"

        if SAVE_TO_FILE:
            start_time = time.time()
            with open("saved_files/" + f, "w") as json_file:
                json.dump({"records": self.data["records"]}, json_file, indent=2)
            print("TIMING: saving to file for", ticker, "took", str(round(time.time() - start_time, 3)) + "s")

        print("Successful")
        return

    @property
    def financial_performance(self):
        return generate_performance_data(self.data["records"])

    def search_asset(self, ticker):
        if not is_internet_connected():
            print("search failed: not connected to the internet.")
            return
        
        # Capitalize
        ticker = ticker.upper()

        ticker_object = yf.Ticker(ticker)

        # Call yfinance to get history data for the past 30 days 
        try:
            start_time = time.time()
            history = ticker_object.history(start=self.date - relativedelta(months=3), end=self.date + timedelta(days=1), interval='1d')
            print("API_TIMING: yfinance call for", ticker, "took", str(round(time.time() - start_time, 3)) + "s")
            daily_data = history['Close']
        except:
            print("search failed: yfinance request failed.")
            return
        
        start_time = time.time()
        info = ticker_object.info
        print("API_TIMING: yfinance info call for", ticker, "took", str(round(time.time() - start_time, 3)) + "s")

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
            print("from_currency", from_currency)
            to_currency = 'USD'
            c = CurrencyRates()

            print("from", from_currency, "to", to_currency)

            # Convert using forex_python
            start_time = time.time()
            rate = c.get_rate(from_currency, to_currency, self.date)
            print("API_TIMING: forex_python call for", ticker, "took", str(round(time.time() - start_time, 3)) + "s")

            print(from_currency, price, "=", to_currency, price * rate )
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
            # other data such as candlestick, price
            'price_chart': price_chart,
            'current_price_usd': dollar_value,
        }

# UTILITY FUNCTIONS
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

def is_internet_connected():
    try:
        response = requests.get("https://www.google.com", timeout=5)
        return response.status_code // 100 == 2
    except requests.ConnectionError:
        return False
