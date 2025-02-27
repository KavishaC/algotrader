import requests
import json
import time

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key

url = 'https://www.alphavantage.co/query?'

# Tinker the parameters later to get optimal result
parameters = {
    "function": "NEWS_SENTIMENT",
    "tickers": "AAPL",
    "sort": "RELEVANCE",
    "apikey": "",
    "time_from": "20220410T0000",
    "time_to": "20220410T2359",
    "limit": "12",
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
print("API_TIMING: alpha vantage call took", str(round(time.time() - start_time, 3)) + "s")

data = r.json()

f = "alpha_news_" + "1" + ".json"

with open(f, "w") as json_file:
    json.dump({"data": data}, json_file, indent=2)
