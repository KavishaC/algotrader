from datetime import datetime, timezone
import yfinance as yf
import pytz
import json

ticker = "AAPL"
tz_ny = pytz.timezone("America/New_York")

start = datetime.fromisoformat("2013-01-04 13:54:00+00:00").astimezone(tz_ny) 
dt = datetime.fromisoformat("2023-01-04 19:33:00+00:00").astimezone(tz_ny) 

end = datetime.fromisoformat("2013-01-05 22:00:00+00:00").astimezone(tz_ny) 
historical_data = yf.Ticker(ticker).history(start=start, end=end, interval='1d')

#with open("record_2_" + ticker + ".txt", "w") as file:
#    file.write("from: " + str(start) + " to: " + str(end))
#    file.write("\nhistorical_data\n")
#    file.write(str(historical_data))


with open("output4.json", "w") as json_file:
    json.dump({"records": historical_data}, json_file, indent=2)