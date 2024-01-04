import json

records = [
    {
      "datetime": "2024-01-04T18:24:00",
      "value": 10,
      "cash": 51.16646485,
      "assets": [
        {
          "price": 10,
          "units": 10,
          "value": 100,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T18:25:00",
      "value": 94.56077962,
      "cash": 34.27419355,
      "assets": [
        {
          "price": 94.56077962,
          "units": 10,
          "value": 945.6077962,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T18:26:00",
      "value": 13.5483871,
      "cash": 45.60296176,
      "assets": [
        {
          "price": 13.5483871,
          "units": 10,
          "value": 135.483871,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T18:27:00",
      "value": 102.043299,
      "cash": 38.70967742,
      "assets": [
        {
          "price": 102.043299,
          "units": 10,
          "value": 1020.43299,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T18:28:00",
      "value": 17.09677419,
      "cash": 51.77419355,
      "assets": [
        {
          "price": 17.09677419,
          "units": 10,
          "value": 170.96774190000002,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T18:29:00",
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
    },
    {
      "datetime": "2024-01-04T18:30:00",
      "value": 20.64516129,
      "cash": 41.37096774,
      "assets": [
        {
          "price": 20.64516129,
          "units": 10,
          "value": 206.45161290000001,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T18:31:00",
      "value": 106.1863637,
      "cash": 20.42289329,
      "assets": [
        {
          "price": 106.1863637,
          "units": 10,
          "value": 1061.863637,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T18:32:00",
      "value": 57.16677042,
      "cash": 50.0,
      "assets": [
        {
          "price": 57.16677042,
          "units": 10,
          "value": 571.6677042,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T18:33:00",
      "value": 25.96774194,
      "cash": 29.71634535,
      "assets": [
        {
          "price": 25.96774194,
          "units": 10,
          "value": 259.6774194,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T18:34:00",
      "value": 113.4682754,
      "cash": 40.48387097,
      "assets": [
        {
          "price": 113.4682754,
          "units": 10,
          "value": 1134.682754,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T18:35:00",
      "value": 40.84578657,
      "cash": 47.28038981,
      "assets": [
        {
          "price": 40.84578657,
          "units": 10,
          "value": 408.4578657,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T18:36:00",
      "value": 31.29032258,
      "cash": 28.06451613,
      "assets": [
        {
          "price": 31.29032258,
          "units": 10,
          "value": 312.90322580000003,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T18:37:00",
      "value": 98.31954778,
      "cash": 54.30958805,
      "assets": [
        {
          "price": 98.31954778,
          "units": 10,
          "value": 983.1954777999999,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T18:38:00",
      "value": 62.89983476,
      "cash": 32.5,
      "assets": [
        {
          "price": 62.89983476,
          "units": 10,
          "value": 628.9983476,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T18:39:00",
      "value": 36.61290323,
      "cash": 30.78174504,
      "assets": [
        {
          "price": 36.61290323,
          "units": 10,
          "value": 366.1290323,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T18:40:00",
      "value": 94.01987821,
      "cash": 45.62388931,
      "assets": [
        {
          "price": 94.01987821,
          "units": 10,
          "value": 940.1987821,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T18:41:00",
      "value": 40.16129032,
      "cash": 51.0216495,
      "assets": [
        {
          "price": 40.16129032,
          "units": 10,
          "value": 401.6129032,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T18:42:00",
      "value": 109.188625,
      "cash": 47.70577439,
      "assets": [
        {
          "price": 109.188625,
          "units": 10,
          "value": 1091.88625,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T18:43:00",
      "value": 65.24511113,
      "cash": 46.69354839,
      "assets": [
        {
          "price": 65.24511113,
          "units": 10,
          "value": 652.4511113,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T18:44:00",
      "value": 45.48387097,
      "cash": 18.30645161,
      "assets": [
        {
          "price": 45.48387097,
          "units": 10,
          "value": 454.8387097,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T18:45:00",
      "value": 47.25806452,
      "cash": 49.99202592,
      "assets": [
        {
          "price": 47.25806452,
          "units": 10,
          "value": 472.5806452,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T18:46:00",
      "value": 59.43269069,
      "cash": 36.93548387,
      "assets": [
        {
          "price": 59.43269069,
          "units": 10,
          "value": 594.3269069,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T18:47:00",
      "value": 50.80645161,
      "cash": 40.23859517,
      "assets": [
        {
          "price": 50.80645161,
          "units": 10,
          "value": 508.06451610000005,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T18:48:00",
      "value": 66.24110061,
      "cash": 52.09964145,
      "assets": [
        {
          "price": 66.24110061,
          "units": 12,
          "value": 794.8932073200001,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T18:49:00",
      "value": 84.28740143,
      "cash": 47.9090884,
      "assets": [
        {
          "price": 84.28740143,
          "units": 12,
          "value": 1011.4488171600001,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T18:50:00",
      "value": 56.12903226,
      "cash": 25.40322581,
      "assets": [
        {
          "price": 56.12903226,
          "units": 12,
          "value": 673.54838712,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T18:51:00",
      "value": 104.1992829,
      "cash": 30.72580645,
      "assets": [
        {
          "price": 104.1992829,
          "units": 12,
          "value": 1250.3913948,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T18:52:00",
      "value": 95.81817681,
      "cash": 30.60296176,
      "assets": [
        {
          "price": 95.81817681,
          "units": 12,
          "value": 1149.81812172,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T18:53:00",
      "value": 61.4516129,
      "cash": 47.0099391,
      "assets": [
        {
          "price": 61.4516129,
          "units": 12,
          "value": 737.4193548000001,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T18:54:00",
      "value": 102.2464177,
      "cash": 47.58064516,
      "assets": [
        {
          "price": 102.2464177,
          "units": 12,
          "value": 1226.9570124,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T18:55:00",
      "value": 65,
      "cash": 8.5483871,
      "assets": [
        {
          "price": 65,
          "units": 12,
          "value": 780,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T18:56:00",
      "value": 90.67075719,
      "cash": 51.9658118,
      "assets": [
        {
          "price": 90.67075719,
          "units": 12,
          "value": 1088.04908628,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T18:57:00",
      "value": 68.5483871,
      "cash": 45.3353786,
      "assets": [
        {
          "price": 68.5483871,
          "units": 20,
          "value": 1370.967742,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T18:58:00",
      "value": 108.6191761,
      "cash": 52.3602293,
      "assets": [
        {
          "price": 108.6191761,
          "units": 20,
          "value": 2172.383522,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T18:59:00",
      "value": 61.56349007,
      "cash": 53.09318185,
      "assets": [
        {
          "price": 61.56349007,
          "units": 20,
          "value": 1231.2698014,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T19:00:00",
      "value": 72.09677419,
      "cash": 5.0,
      "assets": [
        {
          "price": 72.09677419,
          "units": 20,
          "value": 1441.9354838000002,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T19:01:00",
      "value": 73.87096774,
      "cash": 10.32258065,
      "assets": [
        {
          "price": 73.87096774,
          "units": 20,
          "value": 1477.4193547999998,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T19:02:00",
      "value": 70.76554806,
      "cash": 56.7341377,
      "assets": [
        {
          "price": 70.76554806,
          "units": 20,
          "value": 1415.3109612,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T19:03:00",
      "value": 77.41935484,
      "cash": 47.58064516,
      "assets": [
        {
          "price": 77.41935484,
          "units": 20,
          "value": 1548.3870967999999,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T19:04:00",
      "value": 100.9963222,
      "cash": 31.44991738,
      "assets": [
        {
          "price": 100.9963222,
          "units": 20,
          "value": 2019.926444,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T19:05:00",
      "value": 80.96774194,
      "cash": 45.62206176,
      "assets": [
        {
          "price": 80.96774194,
          "units": 20,
          "value": 1619.3548388,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T19:06:00",
      "value": 63.66486156,
      "cash": 45.93548387,
      "assets": [
        {
          "price": 63.66486156,
          "units": 20,
          "value": 1273.2972312,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T19:07:00",
      "value": 82.74193548,
      "cash": 22.74193548,
      "assets": [
        {
          "price": 82.74193548,
          "units": 20,
          "value": 1654.8387096,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T19:08:00",
      "value": 95.01154862,
      "cash": 35.38277403,
      "assets": [
        {
          "price": 95.01154862,
          "units": 20,
          "value": 1900.2309724,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T19:09:00",
      "value": 102.3329297,
      "cash": 51.77419355,
      "assets": [
        {
          "price": 102.3329297,
          "units": 20,
          "value": 2046.658594,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T19:10:00",
      "value": 96.23353649,
      "cash": 12.98387097,
      "assets": [
        {
          "price": 96.23353649,
          "units": 20,
          "value": 1924.6707298000001,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T19:11:00",
      "value": 104.7204586,
      "cash": 28.58338521,
      "assets": [
        {
          "price": 104.7204586,
          "units": 20,
          "value": 2094.409172,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T19:12:00",
      "value": 93.38709677,
      "cash": 41.37096774,
      "assets": [
        {
          "price": 93.38709677,
          "units": 20,
          "value": 1867.7419353999999,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T19:13:00",
      "value": 99.98405184,
      "cash": 23.62903226,
      "assets": [
        {
          "price": 99.98405184,
          "units": 20,
          "value": 1999.6810368000001,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T19:14:00",
      "value": 95.16129032,
      "cash": 18.14516129,
      "assets": [
        {
          "price": 95.16129032,
          "units": 10,
          "value": 951.6129032000001,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T19:15:00",
      "value": 108.7759006,
      "cash": 42.14370072,
      "assets": [
        {
          "price": 108.7759006,
          "units": 10,
          "value": 1087.759006,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T19:16:00",
      "value": 91.24777863,
      "cash": 48.11676824,
      "assets": [
        {
          "price": 91.24777863,
          "units": 10,
          "value": 912.4777862999999,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T19:17:00",
      "value": 103.9316232,
      "cash": 30.88709677,
      "assets": [
        {
          "price": 103.9316232,
          "units": 10,
          "value": 1039.3162320000001,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T19:18:00",
      "value": 100,
      "cash": 50.88709677,
      "assets": [
        {
          "price": 100,
          "units": 30,
          "value": 3000,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T19:19:00",
      "value": 101.7741935,
      "cash": 51.12320885,
      "assets": [
        {
          "price": 101.7741935,
          "units": 30,
          "value": 3053.225805,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T19:20:00",
      "value": 91.20592352,
      "cash": 31.83243078,
      "assets": [
        {
          "price": 91.20592352,
          "units": 30,
          "value": 2736.1777056,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T19:21:00",
      "value": 103.5483871,
      "cash": 30.72580645,
      "assets": [
        {
          "price": 103.5483871,
          "units": 30,
          "value": 3106.451613,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T19:22:00",
      "value": 105.3225806,
      "cash": 53.0,
      "assets": [
        {
          "price": 105.3225806,
          "units": 30,
          "value": 3159.6774179999998,
          "ticker": "AAPL"
        }
      ]
    },
    {
      "datetime": "2024-01-04T19:23:00",
      "value": 105,
      "cash": 47.58064516,
      "assets": [
        {
          "price": 105.3225806,
          "units": 30,
          "value": 3159.6774179999998,
          "ticker": "AAPL"
        }
      ]
    }
  ]

price_data = { 'datetime': [], 'cash': [], 'value': []}

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
            
print("price data:", price_data)