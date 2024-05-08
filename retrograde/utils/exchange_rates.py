import datetime, time
from forex_python.converter import CurrencyRates
import requests
CURRENCY_LAYER_API = '933b1cea4bc571978231a3f0f3373af9'

def get_exchange_rate(from_currency, date):
    to_currency = 'USD'

    print("getting exchange rate from", from_currency, "to", to_currency, "...")

    try:
        start_time = time.time()
        c = CurrencyRates()
        rate = c.get_rate(from_currency, to_currency, date)
        print("API_TIMING: forex_python call took", str(round(time.time() - start_time, 2)) + "s")
        print("forex_python:    returning rate " + from_currency + " to " + to_currency + " as " + str(rate))
        return rate
    
    except Exception as e:
        with open("mylog.txt", "w") as file:
            file.write("forex_python:  getting exchange rate from", from_currency, "to", to_currency, "...")
            file.write("forex_python call failed")

        print("forex_python failed:", e)

    try:
        start_time = time.time()
        params = {'access_key': CURRENCY_LAYER_API, 'source': from_currency, 'currencies': to_currency, date: date.strftime("%Y-%m-%d"), 'format': 1}
        r = requests.get('http://apilayer.net/api/live', params = params)
        livequote = r.json()
        #print(livequote)
        rate = livequote['quotes'][from_currency + to_currency]
        print("API_TIMING: apilayer call for took", str(round(time.time() - start_time, 2)) + "s")
        print("apilayer:        returning rate " + from_currency + " to " + to_currency + " as " + str(rate))
        return rate
    
    except Exception as e:
        with open("mylog.txt", "w") as file:
            file.write("apilayer:      getting exchange rate from", from_currency, "to", to_currency, "...")
            file.write("apilayer call failed")
        print("apilayer failed:", e)


def get_exchange_rate_tester(from_currency, date):
    method = "legacy"
    to_currency = 'USD'

    print("from", from_currency, "to", to_currency)

    #start_time = time.time()

    c = CurrencyRates()
    rate = c.get_rate(from_currency, to_currency, date)
    #print("API_TIMING: forex_python call took", str(round(time.time() - start_time, 2)) + "s")
    print("forex_python:    returning rate " + from_currency + " to " + to_currency + " as " + str(rate))
    
    params = {'access_key': CURRENCY_LAYER_API, 'source': from_currency, 'currencies': to_currency, date: date.strftime("%Y-%m-%d"), 'format': 1}
    r = requests.get('http://apilayer.net/api/live', params = params)
    livequote = r.json()

    #print(livequote)
    rate = livequote['quotes'][from_currency + to_currency]
    print("apilayer:        returning rate " + from_currency + " to " + to_currency + " as " + str(rate))

    #print("API_TIMING: forex apilayer call for took", str(round(time.time() - start_time, 2)) + "s")
    
    return rate

def test1():
    get_exchange_rate("JPY", datetime.date.today())
    get_exchange_rate("JPY", datetime.date.today() - datetime.timedelta(days=365))
    get_exchange_rate("EUR", datetime.date.today())
    get_exchange_rate("EUR", datetime.date.today() - datetime.timedelta(days=365))