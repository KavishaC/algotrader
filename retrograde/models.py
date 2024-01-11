from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from .data import price_data
import json
import yfinance as yf
from .read_stock_prices import get_price
import pandas as pd
import os
from openai import OpenAI
from .financial_performance import generate_performance_data
import threading
import html
from .asset_charts import get_candlestick_data
from forex_python.converter import CurrencyRates

class User(AbstractUser):
    timezone = models.CharField(max_length=50, default='UTC')

#account_balance = models.DecimalField(max_digits=8, decimal_places=2)# summation of all portfolios owned by user

"""
Creates a portfolio in an unique spacetime. "Colombo, 13th september 2020". Smallest measure of time is a minute.
"""
class Portfolio(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey("User", on_delete=models.PROTECT, related_name="portfolios")
    date = models.DateField()
    data = models.JSONField(default=dict, blank=True)
    initial_capital = models.DecimalField(max_digits=12, decimal_places=0, blank=False, default=0) # define the max length of an asset
    #TODO time_scale =  DAY,WEEK, MONTH, YEAR
    #TODO:AutoPilot #strategy = models.ForeignKey("Strategy", on_delete=models.PROTECT)
    advice = models.CharField(max_length=1000, blank=True)
    asset_data = models.JSONField(default=dict, blank=True)

    """
    Get chart data from records
    """
    @property
    def price_data(self):
        print("reading price data...")
        records = Portfolio.objects.get(pk=self.id).data["records"]
        #print("last record", records[-1])
        #print("records:", records)
        price_data = { 'date': [], 'value': [], 'cash': []}
        #print("last_record (calling from price_data):", records[-1])
        assets = []

        for record in records:
            for asset_record in record['assets']:
                if asset_record['ticker'] not in assets:
                    assets.append(asset_record["ticker"])
                    price_data[asset_record["ticker"]] = []

        for record in records:
            price_data['date'].append(record["date"])
            price_data['cash'].append(record["cash"])
            price_data['value'].append(record["value"])

            for asset in assets:
                value = None
                for asset_record in record["assets"]:
                    if asset_record["ticker"] == asset:
                        value = asset_record["value"]
                price_data[asset].append(value)

        # TODO replace zeros with None objects so that lines won't be rendered on the t axis
        return json.dumps(price_data)

    """
    Get asset data
    """
    @property
    def asset_data(self):
        print("generating asset data...")
        # okay so self.data["records"] had a record missing. It wasn't a problem with saving but with retrieving.
        # For now use the following method repalce it later
        current_record = Portfolio.objects.get(pk=self.id).data["records"][-1]

        assets = current_record["assets"]
        data = []
        index = 0;
        for asset in assets:
            ticker = asset["ticker"]
            #print("getting history for", ticker, "from", self.date - timedelta(days=30), self.date + timedelta(days=1))
            tickerObject = yf.Ticker(ticker)
            history = tickerObject.history(start=self.date - timedelta(days=30), end=self.date + timedelta(days=1), interval='1d')
            daily_data = history['Close']
            info = tickerObject.info

            long_name = info.get('longName', '')
            if (ticker=="GC=F"):
                long_name = "Gold"

            current_price_change = percentage_change(get_price(self.date, daily_data), get_price(self.date - timedelta(days=1), daily_data))
            data.append({
                'index': str(index),
                'country': info.get('country', ''),
                'ticker': ticker,
                'quote_type': info.get('quoteType', ''),
                'currency': info.get('currency', ''),
                'exchange': info.get('exchange', ''),
                'long_business_summary': info.get('longBusinessSummary', 'Not available.'),
                'long_name': long_name, # not everything has it
                'current_price': "{:.2f}".format(get_price(self.date, daily_data)),
                'current_price_change': current_price_change,
                'current_price_change_status': percentage_change_status(current_price_change),
                'current_num_units': asset['units'],
                'current_value': "{:.2f}".format(asset['value']),
                'current_value_percent': "{:.2f}".format(asset['value'] * 100 / current_record['value']) + "%",
                'price_chart': [],
                'candlestick_chart': json.dumps(asset_chart[1]),
                'num_units_chart': json.dumps(asset_chart[0]),
            })
            # 
            index += 1

        data = sorted(data, key=lambda x: float(x['current_value']), reverse=True)
        data.append({
            'index': str(index),
            'ticker': "Cash",
            'current_value': "{:.2f}".format(current_record['cash']),
            'current_value_percent': "{:.2f}".format(current_record['cash'] * 100 / current_record['value']) + "%",
            'candlestick_chart': json.dumps(asset_chart[1]),
            'num_units_chart': json.dumps(asset_chart[0])
        })

        return data

    @property
    def value(self):
        records = self.data["records"]
        return "{:.2f}".format(records[-1]["value"])

    @property
    def change(self):
        records = self.data["records"]
        today = records[-1]["value"]
        yesterday = records[-2]["value"]
        change_percent = ((today-yesterday)/yesterday) * 100
        change_percent_str = "{:.2f}".format(change_percent)
        if (change_percent > 0 and change_percent_str != "0.00"):
            change_percent_str = "+" + change_percent_str
        if (change_percent_str == "-0.00"):
            change_percent_str = change_percent_str[1:]
        return change_percent_str + "%"
    
    @property
    def change_status(self):
        return percentage_change_status(self.change)

    def save(self, *args, **kwargs):
        if not self.pk:
            # For new portfolios
            self.data = {"records": [{
                "date": datetime.now().date().isoformat(),
                "value": float(self.capital),
                "cash": float(self.capital),
                "assets": []
            }]}
        super().save(*args, **kwargs)

    def tick(self, tick_timedelta_str):
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

        # update each asset record so that records are available upto portfolio datetime
        self.date = dt
        self.update()

        # save changes to database
        #self.generate_advice()
        self.save()

    """
    Update records upto portfolio datetime
    """
    def update(self):
        print("updating records...")
        #with self.method_lock:
        last_record = self.data["records"][-1]
        record_date = datetime.fromisoformat(last_record["date"]).date()
        portfolio_date = self.date

        ticker_histories = {}

        #print("Writing records upto present time of portfolio")

        # write missing records
        while (record_date < portfolio_date):
            #print("reading last_record[datetime]: ", record_date, "not yet at current_time :", portfolio_date)

            # generate record for next day
            record_date += timedelta(days=1)
            next_record = {
                "date": record_date.isoformat(),
                "cash": last_record["cash"], # copy the cash forward
                "assets": []
            }

            value = next_record["cash"]
            for asset in last_record["assets"]:
                ticker = asset["ticker"]

                if ticker not in ticker_histories:
                    # copy daily data from next record upto portfolio datetime
                    daily_data = yf.Ticker(ticker).history(start=record_date - timedelta(days=30), end=portfolio_date + timedelta(days=2), interval='1d')['Close']
                    #print("daily_data:", daily_data)
                    
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
                    new_asset_record["currency"] = asset['currency']
                    from_currency = asset['currency']
                    to_currency = 'USD'

                    c = CurrencyRates()
                    rate = c.get_rate(from_currency, to_currency, record_date)
                    print("from", from_currency, "to", to_currency)
                    print(from_currency, current_price, "=", to_currency, current_price * rate )

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
        # save changes
        self.save()

        # save to file
        f = "server_portfolio_records_" + str(self.id) + ".json"
        with open(f, "w") as json_file:
            json.dump({"records": self.data["records"]}, json_file, indent=2)
        #print("done updating records...")

    def generate_advice(self):
        # we recommend using python-dotenv to add OPENAI_API_KEY="My API Key" to your .env file
        # so that your API Key is not stored in source control.
        client = OpenAI(api_key="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",)
        advice = [
            "If there is a way to improve the portfolio give feedback. If you think there is no Otherwise some fact the market trends of the asset held in the portfolio.",
            "Give me some random piece of investment advice relevant to my portfolio. Value the portion of the investment based on their values."
        ]
        start = advice[1]
        
        start += " Limit your response to 30 words.\n"
        
        last_record = Portfolio.objects.get(pk=self.id).data["records"][-1]
        request = start + str(last_record)
        print("Request:", start)
        chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": request,
            }],
            model="gpt-3.5-turbo",
        )
        #print("AI response object:", chat_completion)
        first_choice = chat_completion.choices[0]
        content = first_choice.message.content
        content = html.escape(content)
        print("Response:", content)
        with open('AI_feedback.txt', 'a') as file:
            # Add text to the file
            file.write("Q: " + start + '\n')
            file.write("A: " + content + '\n\n\n')

        self.advice = content.replace("\n", "").replace("EOF", "")
        self.save()

    """
    Updated the most recent record. Minus cash plus units plus value plus port value
    """
    def buy(self, ticker, num_units):
        print("buy:", ticker, "num_units:", num_units)

        price = None
        existing_asset = False
        last_record = self.data["records"].pop()
        #print("last_record", last_record)
        for asset in last_record['assets']:
            convert = False
            if asset['ticker'] == ticker:
                existing_asset = True
                price = asset['price']
                if ('currency' in asset):
                    convert = True
                    from_currency = asset['currency']

        if price == None:
            ticker_object = yf.Ticker(ticker)
            daily_data = ticker_object.history(start=self.date - timedelta(days=15), end=self.date + timedelta(days=1), interval='1d')['Close']
            price = get_price(self.date, daily_data)
            if 'currency' in ticker_object.info:
                from_currency = ticker_object.info['currency']
                print("from_currency", from_currency)
                if from_currency != "USD":
                    convert = True

        purchase_value = num_units * price

        if convert:
            to_currency = 'USD'
            print("from", from_currency, "to", to_currency)

            c = CurrencyRates()
            rate = c.get_rate(from_currency, to_currency, self.date)
            print(from_currency, price, "=", to_currency, price * rate )
            purchase_value *= rate

        #print("purchase value = price * num_units = ", price, num_units, "=", purchase_value, "<", 'cash_balance', last_record["cash"])
        if last_record["cash"] < purchase_value:
            print("Cash balance not adequate for transaction")
            return "Cash balance not adequate for transaction"

        # 1. deduct cash balance
        last_record['cash'] -= purchase_value

        # 2. add new units record for current datetime

        if existing_asset:
            for asset in last_record['assets']:
                if asset['ticker'] == ticker:
                    asset['units'] += num_units
                    asset['value'] += purchase_value
        else:
            asset = {
                "price": price,
                "units": num_units,
                "value": purchase_value,
                "ticker": ticker
            }
            if convert:
                asset['currency'] = from_currency
            last_record['assets'].append(asset)
        
        # 3. update_volume
        self.data["records"].append(last_record)
        self.save()
        #self.generate_advice()

        print("successful buy")
        # save to file
        f = "server_portfolio_records_" + str(self.id) + ".json"
        with open(f, "w") as json_file:
            json.dump({"records": self.data["records"]}, json_file, indent=2)

        return "successful"

    def sell(self, ticker, num_units):
        print("sell:", ticker, "num_units:", num_units)
        existing_asset = False
        last_record = self.data["records"].pop()

        for asset in last_record['assets']:
            if asset['ticker'] == ticker:
                existing_asset = True
                price = asset['price']
                units = asset['units']
                if units < num_units:
                    print("do not own asset. Cannot complete transaction")
                    return "do not own asset. Cannot complete transaction"
                asset['units'] -= num_units
                purchase_value = price * num_units
                if "currency" in asset:
                    from_currency = asset["currency"]
                    to_currency = 'USD'
                    print("from", from_currency, "to", to_currency)
                    print(from_currency, price, "=", to_currency, price * rate )

                    c = CurrencyRates()
                    rate = c.get_rate(from_currency, to_currency, self.date)
                    purchase_value *= rate

                asset['value'] -= purchase_value
                last_record["cash"] += purchase_value
        
        if existing_asset == False:
            print("do not own asset. Cannot complete transaction")

            return "do not own asset. Cannot complete transaction"
        last_record['assets'] = [item for item in last_record['assets'] if item['units'] != 0]

        self.data["records"].append(last_record)
        self.save()
        #self.generate_advice()
    
        print("successful")
        # save to file
        f = "server_portfolio_records_" + str(self.id) + ".json"
        with open(f, "w") as json_file:
            json.dump({"records": self.data["records"]}, json_file, indent=2)

        return "successful"

    @property
    def financial_performance(self):
        return generate_performance_data(self.data["records"])
"""
Percentage change value2 => value1
"""
def percentage_change(value1, value2):
    change_percent = ((value1-value2)/value2) * 100
    change_percent_str = "{:.2f}".format(change_percent)
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

#"""
#Constantly updates its data to exist in parallel with the portfolio spacetime
#"""
#class AssetRecord(models.Model):
#    ticker = models.CharField(max_length=100)
#    portfolio = models.ForeignKey("Portfolio", on_delete=models.PROTECT, related_name="asset_records")
#
#"""
#Finds the current(in portfolio spacetime) price of the asset
#"""
#
#"""
#Add record for each minute upto current minute matching spacetime of portfolio.
#Update price column using yfinance and then value column according to units.
#"""
#def update(self):
#        # read datetime from portfolio
#        # use yfinance to get data and update price column
#        # update value column based on data
#        pass

    
# class Asset:
#     name = models.CharField(max_length=100) # define max length of an asset
#     description = models.CharField(max_length=100) # define max length of a description 
    
#     @property
#     def get_price(self, time):
#         return # check the price of the asset at the time and display it

# class PriceRecord:
#     asset = models.ForeignKey("Asset", on_delete=models.PROTECT, related_name="price_records")
#     datetime = models.DateTimeField() # define if null exists or not
#     price = models.DecimalField(max_digits=10, decimal_places=2) # define the max length of an asset

# class AssetRecord:
#     asset = models.ForeignKey("Asset", on_delete=models.PROTECT, related_name="asset_records")
#     portfolio = models.ForeignKey("Portfolio", on_delete=models.PROTECT, related_name="asset_records")
#     price = models.DecimalField(max_digits=10, decimal_places=2) # define the max length of an asset
#     num_units = models.DecimalField(max_digits=10, decimal_places=2)

#     @property
#     def get_value(self, time):
#         return # calculate the value from num_units
    
# class Strategy:
#     pass

# class CustomStrategy(Strategy):
#     custom_field = models.CharField(max_length=255)
#     # additional fields or methods specific to the custom strategy

#     def apply_strategy(self):
#         # custom implementation of the strategy
#         pass

#     def __str__(self):
#         return f"{self.name} - Custom Strategy"
    
asset_chart = [{
                'type': "line",
                'label': "AAPL",
                'yAxisID': "y_line",
                'borderColor': 'rgba(255, 165, 0, 1)',
                'borderWidth': 3,
                'pointRadius': 10,
                'pointBorderColor': 'rgba(100, 220, 150, 0)',
                'pointBackgroundColor': 'rgba(100, 220, 150, 0)',
                'pointHoverRadius': 10,
                'pointHoverBackgroundColor': 'rgba(255, 165, 0, 1)',
                'pointHoverBorderColor': 'rgba(255, 165, 0, 1)',
                'stepped': True,
                'data': [
                {
                  'x': 1491004800000,
                  'y': 10
                },
                {
                  'x': 1491177600000,
                  'y': 10
                },
                {
                  'x': 1491264000000,
                  'y': 15
                },
                {
                  'x': 1491350400000,
                  'y': 15
                },
                {
                  'x': 1491436800000,
                  'y': 15
                },
                {
                  'x': 1491523200000,
                  'y': 15
                },
                {
                  'x': 1491782400000,
                  'y': 10
                },
                {
                  'x': 1491868800000,
                  'y': 10
                },
                {
                  'x': 1491955200000,
                  'y': 10
                },
                {
                  'x': 1492041600000,
                  'y': 10
                }
                ],
              },
              { 
                'type': 'candlestick',
                'label': 'Volume',
                'yAxisID': "y_candlestick",
                'data': [
                {'x': 1491004800000, 'o': 28.92, 'h': 31.07, 'l': 26.43, 'c': 29.51},
                {'x': 1491177600000, 'o': None, 'h': None, 'l': None, 'c': None},
                {'x': 1491264000000, 'o': 29.17, 'h': 32.31, 'l': 28.84, 'c': 29.41},
                {'x': 1491350400000, 'o': 30.59, 'h': 31.62, 'l': 27.48, 'c': 30.05},
                {'x': 1491436800000, 'o': 29.82, 'h': 30.8, 'l': 28.39, 'c': 30.22},
                {'x': 1491523200000, 'o': 29.1, 'h': 30.35, 'l': 26.42, 'c': 29.3},
                {'x': 1491782400000, 'o': 29.61, 'h': 32, 'l': 26.55, 'c': 29.23},
                {'x': 1491868800000, 'o': 28.41, 'h': 29.53, 'l': 27.93, 'c': 28.33},
                {'x': 1491955200000, 'o': 27.9, 'h': 29.36, 'l': 25.93, 'c': 27.84},
                {'x': 1492041600000, 'o': 26.76, 'h': 28.26, 'l': 23.69, 'c': 26.14},
                ]
              }]