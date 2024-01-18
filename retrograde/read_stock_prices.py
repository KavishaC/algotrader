import yfinance as yf
from datetime import datetime, timezone, timedelta
import pandas as pd
import pytz, json
from dateutil.relativedelta import relativedelta

#tickers = ["AAPL", "DJIA"]
#tz_ny = pytz.timezone("America/New_York")
#
#for ticker in tickers:
#    start = datetime.fromisoformat("2024-01-04 13:54:00+00:00").astimezone(tz_ny) 
#    dt = datetime.fromisoformat("2024-01-04 19:33:00+00:00").astimezone(tz_ny) 
#
#    end = datetime.fromisoformat("2024-01-04 22:00:00+00:00").astimezone(tz_ny) 
#    historical_data = yf.Ticker(ticker).history(start=start, end=end, interval='1m')
#
#    try:
#        resampled_data = historical_data['Close'].resample('1T').ffill()
#    except:
#        historical_data.index = pd.to_datetime(historical_data.index)
#
#    # creates a record for each minute by 
#    #print("start tz", start.tzinfo, "sampled", resampled_data.index[0].tzinfo)
#    # Generate timestamps from start_date to the first record in historical_data
#    start_gap_data = pd.Series(index=pd.date_range(start=start, end=resampled_data.index[0], freq='1T'))
#
#    # Generate timestamps from the last record in historical_data to end_date
#    end_gap_data = pd.Series(index=pd.date_range(start=resampled_data.index[-1], end=end, freq='1T'))
#
#    # Concatenate all data together
#    combined_data = pd.concat([start_gap_data, resampled_data, end_gap_data])
#
#    # Forward-fill missing values from start_date and back-fill missing values from end_date
#    combined_data.ffill(inplace=True)
#    combined_data.bfill(inplace=True)
#    combined_data.to_csv('combined_data_2.csv', header=True)
#    with open("record_" + ticker + ".txt", "w") as file:
#        file.write("from: " + str(start) + " to: " + str(end))
#        file.write("\nhistorical_data\n")
#        file.write(str(historical_data))
#        file.write("\nresampled\n")
#        file.write(str(resampled_data))
#        file.write("\ngaps filled\n")
#        file.write(str(combined_data))
#        file.write("\n\nlooking for" + str(dt) + "\n")
#        file.write(str(float(combined_data.loc[dt])) + str(type(combined_data.loc[dt])))
#
#
#def gap_filled_records(start, end, ticker):
#    historical_data = yf.Ticker(ticker).history(start=start, end=end, interval='1m')
#    # creates a record for each minute by 
#
#    historical_data.index = pd.to_datetime(historical_data.index)
#    resampled_data = historical_data['Close'].resample('1T').ffill()
#    print("start tz", start.tzinfo, "sampled", resampled_data.index[0].tzinfo)
#    # Generate timestamps from start_date to the first record in historical_data
#    tz = resampled_data.index[0].tzinfo
#    start = start.astimezone(tz) 
#    end = end.astimezone(tz) 
#
#    start_gap_data = pd.Series(index=pd.date_range(start=start, end=resampled_data.index[0], freq='1T'))
#
#    # Generate timestamps from the last record in historical_data to end_date
#    end_gap_data = pd.Series(index=pd.date_range(start=resampled_data.index[-1], end=end, freq='1T'))
#
#    # Concatenate all data together
#    combined_data = pd.concat([start_gap_data, resampled_data, end_gap_data])
#
#    # Forward-fill missing values from start_date and back-fill missing values from end_date
#    combined_data.ffill(inplace=True)
#    combined_data.bfill(inplace=True)
#
#    with open("record_" + ticker + ".txt", "w") as file:
#        file.write("from: " + str(start) + " to: " + str(end))
#        file.write("\nhistorical_data\n")
#        file.write(str(historical_data))
#        file.write("\nresampled\n")
#        file.write(str(resampled_data))
#        file.write("\ngaps filled\n")
#        file.write(str(combined_data))    
#
#    return combined_data

def get_price(dt, daily_data):
    # type(daily_data) is <class 'pandas.core.frame.DataFrame'>
    #print("looking for price for:", dt)
    #print("daily data:", daily_data)
    try:
        daily_data.index = daily_data.index.date
    except:
        pass

    while True:
        if dt in daily_data.index:
            #print("price found :", daily_data[dt])
            return daily_data[dt]
        dt -= timedelta(days=1)

def get_price_chart(daily_data, current_date):

    price_chart = {
        'date': [],
        'price': [],
    }
    try:
        daily_data.index = daily_data.index.date
    except:
        pass

    first_date = current_date - relativedelta(months=3)
    #print("generating price data for 3 months from", first_date, "leading to", current_date, "from history\n", daily_data)

    dt = first_date
    while (dt <= current_date):
        #print("generating record for", dt)

        record_dt = dt
        while True:
            #print("    checking", record_dt)
            if record_dt in daily_data.index:
                #print("    found date", record_dt)
                price = daily_data[record_dt]
                break
            if (record_dt < first_date):
                #print("    date beyond first")
                price = None
                break
            record_dt -= timedelta(days=1)

        #print("adding data date:", dt, "price:", price)

        price_chart['date'].append(dt.isoformat())
        price_chart['price'].append(price)
        dt += timedelta(days=1)
    
    if False:
        print("\nprice_chart:")
        i = 0
        for date in price_chart['date']:
            if date in daily_data.index:
                price = daily_data[date]
            else:
                price = None
            print(date, "\t", price_chart['price'][i] , "\t", price)
            i += 1
    return json.dumps(price_chart)