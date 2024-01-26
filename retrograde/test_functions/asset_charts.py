

def get_candlestick_data(today, history):
    try:
        history.index = history.index.date
    except:
        pass

    while True:
        if dt in daily_data.index:
            #print("price found :", daily_data[dt])
            return daily_data[dt]
        dt -= timedelta(days=1)