import datetime, time
from forex_python.converter import CurrencyRates
import requests
CURRENCY_LAYER_API = '933b1cea4bc571978231a3f0f3373af9'
ALPHAVANTAGE_API = "V3UO2MUD5E7I896L"
from .ddofborg import get_exchange_rates

"""
This is the function used by server to get exchange rates. Has to work all the time.
"""
def get_exchange_rate(from_currency, date):
    to_currency = 'USD'

    print("getting exchange rate from", from_currency, "to", to_currency, "...")
    return get_ddofborg_exchange_rate(from_currency, to_currency, date)

"""
FOREX_PYTHON
This used to work but now only works half the time. The reason why the website crashed.
"""
def get_forexpython_exchange_rate(from_currency, to_currency, date):
    start_time = time.time()

    c = CurrencyRates()
    rate = c.get_rate(from_currency, to_currency, date)
    print("apilayer:        returning rate " + from_currency + " to " + to_currency + " on " +  str(date) + " as " + str(rate))
    
    print("API_TIMING: forexpython call for took", str(round(time.time() - start_time, 2)) + "s")
    return rate

"""
API_LAYER
Couldn't figure out how to get historical rates. Paid.
"""
def get_apilayer_exchange_rate(from_currency, to_currency, date):
    start_time = time.time()
    print("date", date.strftime("%Y-%m-%d"))
    params = {'access_key': CURRENCY_LAYER_API, 'source': from_currency, 'currencies': to_currency, date: date.strftime("%Y-%m-%d"), 'format': 1}
    r = requests.get('http://apilayer.net/api/historical', params = params)
    livequote = r.json()

    print(livequote)
    rate = livequote['quotes'][from_currency + to_currency]
    rate_date = datetime.datetime.fromtimestamp(livequote['timestamp'], tz=datetime.timezone.utc)
    print("apilayer:        returning rate " + from_currency + " to " + to_currency + " on " +  str(rate_date) + " as " + str(rate))
    
    print("API_TIMING: apilayer call for took", str(round(time.time() - start_time, 2)) + "s")
    return rate

"""
CURRENCY_LAYER
Only has support for year 1999-01-01 and onwards. $14 a month.
"""
def get_currencylayer_exchange_rate(from_currency, to_currency, date):

    start_time = time.time()
    print("date", date.strftime("%Y-%m-%d"))
    params = {'access_key': CURRENCY_LAYER_API, 'source': from_currency, 'currencies': to_currency, 'date': date.strftime("%Y-%m-%d"), 'format': 1}
    r = requests.get('http://api.currencylayer.com/historical?', params = params)
    print(r.url)
    print(r)

    # Check if the request was successful
    if r.status_code == 200:
        response_data = r.json()
        if response_data.get("success"):
            print("Request was successful.")
        else:
            error_info = response_data.get("error", {}).get("info", "Unknown error")
            print(f"Request failed: {error_info}")
    else:
        print(f"Request failed with status code: {r.status_code}")

    livequote = r.json()

    print(livequote)

    rate = livequote['quotes'][from_currency + to_currency]
    rate_date = datetime.datetime.fromtimestamp(livequote['timestamp'], tz=datetime.timezone.utc)
    print("currrencylayer:        returning rate " + from_currency + " to " + to_currency + " on " +  str(rate_date) + " as " + str(rate))
    
    print("API_TIMING: currency call for took", str(round(time.time() - start_time, 2)) + "s")
    return rate

"""
DDOFBORG
Only has support for year 1999-01-01 and onwards. Free. Fast (0.10s).
Worked and was best option on 14 May 2024 
"""
def get_ddofborg_exchange_rate(from_currency, to_currency, date):
    start_time = time.time()

    rates = get_exchange_rates(from_currency, target_currencies=[to_currency], on_date=date.strftime("%Y-%m-%d"))

    #print(rates)
    rate = rates['USD']
    print("ddofborg: " + str(round(time.time() - start_time, 2)) + "s" + " returning rate " + from_currency + " to " + to_currency + " on " +  str(date) + " as " + str(rate))
    #print("API_TIMING: ddofborg call took", str(round(time.time() - start_time, 2)) + "s")

    return rate

"""
ALPHA_VANTAGE
Not the best as it does not support rates before 2000's. Maybe use for realtime rates in future applications. Currently gives realtime.
"""
def get_alphavantage_exchange_rate(from_currency, to_currency, date):
    url = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&'
    url += 'from_currency=' + from_currency + '&'
    url += 'to_currency=' + to_currency + '&'
    url += 'apikey=' + ALPHAVANTAGE_API

    r = requests.get(url)
    data = r.json()
    print(data)

"""
Testing function to test each of the APIs
"""
def exchange_rate_tester(from_currency, date):
    to_currency = 'USD'

    print("requesting exchange rate from", from_currency, "to", to_currency, "for", date)

    get_ddofborg_exchange_rate(from_currency, to_currency, date)
    return 

"""
exchange_rate_tester("EUR", datetime.date.today())
#time.sleep(1)
exchange_rate_tester("EUR", datetime.datetime.strptime("2000-01-01", "%Y-%m-%d").date())
#time.sleep(1)
exchange_rate_tester("EUR", datetime.datetime.strptime("1999-01-01", "%Y-%m-%d").date())
#time.sleep(1)
exchange_rate_tester("JPY", datetime.date.today())
#time.sleep(1)
exchange_rate_tester("JPY", datetime.datetime.strptime("2000-01-01", "%Y-%m-%d").date())
#time.sleep(1)
exchange_rate_tester("JPY", datetime.datetime.strptime("1999-01-01", "%Y-%m-%d").date())

exchange_rate_tester("GBP", datetime.datetime.strptime("1999-01-01", "%Y-%m-%d").date())

"""
