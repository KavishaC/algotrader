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
    #strategy = models.ForeignKey("Strategy", on_delete=models.PROTECT)

    """
    Get chart data from records
    """
    @property
    def price_data(self):
        records = self.data["records"]
        price_data = { 'date': [], 'value': [], 'cash': []}
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

    @property
    def value(self):
        records = self.data["records"]
        return "{:.2f}".format(records[-1]["value"])

    @property
    def change(self):
        # TODO
        return "+0.02%"
    
    @property
    def change_status(self):
        # TODO
        return "POSITIVE"

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
        self.date = dt

        # update each asset record so that records are available upto portfolio datetime
        self.update()

        # save changes to database
        self.save()

    """
    Update records upto portfolio datetime
    """
    def update(self):
        records = self.data["records"]
        most_recent_record = records[-1]
        most_recent_record_date = datetime.fromisoformat(most_recent_record["date"]).date()
        portfolio_date = self.date

        ticker_histories = {}

        print("Writing records upto present time of portfolio")

        # write missing records
        while (most_recent_record_date <= portfolio_date):
            print("reading most_recent_record[datetime]: ", most_recent_record_date, "not yet at current_time :", portfolio_date)

            # generate record for next day
            most_recent_record_date += timedelta(days=1)
            next_record = {
                "date": most_recent_record_date.isoformat(),
                "cash": most_recent_record["cash"], # copy the cash forward
                "assets": []
            }

            value = 0
            for asset in most_recent_record["assets"]:
                ticker = asset["ticker"]

                if ticker not in ticker_histories:
                    # copy daily data from next record upto portfolio datetime
                    daily_data = yf.Ticker(ticker).history(start=most_recent_record_date - timedelta(days=30), end=portfolio_date, interval='1d')['Close']
                    print("daily_data:", daily_data)
                    
                    ticker_histories[ticker] = daily_data

                # create asset record
                current_price = get_price(most_recent_record_date, daily_data)
                new_asset_record = {
                    "ticker": ticker,
                    "units": asset["units"],
                    "price": current_price,
                    "value": asset["units"] * current_price
                }
                value += new_asset_record["value"]
                next_record["assets"].append(new_asset_record)

            # update rest of portfolio record
            next_record["value"] = value
            records.append(next_record)
            most_recent_record = next_record

        # save changes
        self.data["records"] = records
        self.save()

        # save to file
        f = "server_portfolio_records_" + str(self.id) + ".json"
        with open(f, "w") as json_file:
            json.dump({"records": records}, json_file, indent=2)

    """
    Get current price of an asset
    """
    @property
    def current_price(self, ticker):
        # retrieve price from latest record
        return round(self.data["records"][-1]["value"], 2)

    @property
    def current_units(self, ticker):
        # retrieve volume from latest record
        pass

    @property
    def current_value(self, ticker):
        # retrieve value from latest record
        pass
    
    """
    Updated the most recent record. Minus cash plus units plus value plus port value
    """
    def buy(self, ticker, num_units):
        # 1. deduct cash balance
        # 2. add new units record for current datetime
        # 3. update_volume
        pass

    def sell(self, ticker, num_units):
        # 1. check units balance
        # 2. increase cash balance
        # 3. update most recent record
        pass

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