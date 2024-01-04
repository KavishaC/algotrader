from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from .data import price_data
import json

class User(AbstractUser):
    pass

#account_balance = models.DecimalField(max_digits=8, decimal_places=2)# summation of all portfolios owned by user

"""
Creates a portfolio in an unique spacetime. "Colombo, 13th september 2020". Smallest measure of time is a minute.
"""
class Portfolio(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey("User", on_delete=models.PROTECT, related_name="portfolios")
    now_datetime = models.DateTimeField(blank= True, null=True)
    #strategy = models.ForeignKey("Strategy", on_delete=models.PROTECT) #assosiated strategy
    data = models.JSONField(default=dict, blank=True) # cash field can be used to track 

    @property
    def price_data(self):

        # find earliest date
        records = self.data["records"]

        price_data = { 'datetime': [], 'value': [], 'cash': []}

        assets = []

        for record in records:
            for asset_record in record['assets']:
                if asset_record['ticker'] not in assets:
                    assets.append(asset_record["ticker"])
                    price_data[asset_record["ticker"]] = []

        for record in records:
            price_data['datetime'].append(record["datetime"])
            price_data['cash'].append(record["cash"])
            price_data['value'].append(record["value"])

            for asset in assets:
                value = None
                for asset_record in record["assets"]:
                    if asset_record["ticker"] == asset:
                        value = asset_record["value"]
                price_data[asset].append(value)
                    
        #print("price data:", price_data)

        return json.dumps(price_data)

    @property
    def value(self):
        records = self.data["records"]
        #print("records", records)
        return "{:.2f}".format(records[-1]["value"])

    @property
    def change(self):
        return "+0.02%"
    
    @property
    def change_status(self):
        return "POSITIVE"

    def save(self, *args, **kwargs):
        if not self.pk:  # Check if it's a new record
            self.now_datetime = timezone.now()
        super().save(*args, **kwargs)
        self.now_datetime = self.now_datetime.replace(second=0, microsecond=0)
        # add a cash record

    def tick(self, tick_timedelta_str):
        # just for safety
        dt = self.now_datetime
        self.now_datetime = dt.replace(second=0, microsecond=0)
        print(dt.replace(second=0, microsecond=0)) 

        if (tick_timedelta_str == "1m"):
            dt += timedelta(minutes=1)
        elif (tick_timedelta_str == "5m"):
            #round up to next 5 mins
            dt += timedelta(minutes=(5 - dt.minute % 5))
        elif (tick_timedelta_str == "15m"):
            #round up to next 15 mins
            dt += timedelta(minutes=(15 - dt.minute % 15))
        elif (tick_timedelta_str == "30m"):
            dt += timedelta(minutes=(30 - dt.minute % 30))
        elif (tick_timedelta_str == "1h"):
            dt = datetime.now().replace(minute=0)
            dt += timedelta(hours=1)
        elif (tick_timedelta_str == "1d"):
            dt = datetime.now().replace(hours=0)
            dt += timedelta(days=1)
        elif (tick_timedelta_str == "1wk"):
            dt += timedelta(days=(7 - dt.weekday()))
        elif (tick_timedelta_str == "1mo"):
            dt += relativedelta(months=1)
            dt.replace(day=1)

        """elif (tick_timedelta_str == "3mo"):
            tick_timedelta = timedelta(hours=1)
        elif (tick_timedelta_str == "6mo"):
            tick_timedelta = timedelta(hours=1)
        elif (tick_timedelta_str == "1y"):
            tick_timedelta = timedelta(hours=1) """
        
        # update each asset record so that data is available upto portfolio datetime
        self.update()
        self.now_datetime = dt
        self.save()

    def update(self):
        records = self.data["records"]
        most_recent_record = records[-1]
        current_time = self.now_datetime
        while (datetime.fromisoformat(most_recent_record["datetime"]) != datetime.fromisoformat(current_time.replace(tzinfo=None).isoformat())):
            time_str = most_recent_record["datetime"]
            print("most_recent_record[datetime]: ", time_str, "== current_time :", current_time)
            time = datetime.fromisoformat(time_str)
            time += timedelta(minutes=1)
            next_record = {
                "datetime": time.isoformat(),
                "value": 80.47719034,
                "cash": 32.62255557,
                "assets": [
                    {
                    "price": 80.47719034,
                    "units": 10,
                    "value": 804.7719034,
                    "ticker": "AAPL"
                    }
                ]
            }
            records.append(next_record)
            most_recent_record = next_record
        #print(records)
        self.data["records"] = records
        print(self.data)
        self.save()

    @property
    def current_price(self, ticker):
        # retrieve price from latest record
        pass

    @property
    def current_units(self, ticker):
        # retrieve volume from latest record
        pass

    @property
    def current_value(self, ticker):
        # retrieve value from latest record
        pass
    
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

    """ for asset_record in asset_records:
        asset_record.update() """

        # now use the asset values to update value in cash_and_value 

"""
Constantly updates its data to exist in parallel with the portfolio spacetime
"""
""" class AssetRecord(models.Model):
    ticker = models.CharField(max_length=100)
    portfolio = models.ForeignKey("Portfolio", on_delete=models.PROTECT, related_name="asset_records")
"""
"""
Finds the current(in portfolio spacetime) price of the asset
"""

"""
Add record for each minute upto current minute matching spacetime of portfolio.
Update price column using yfinance and then value column according to units.
"""
"""     def update(self):
        # read datetime from portfolio
        # use yfinance to get data and update price column
        # update value column based on data
        pass """

    
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