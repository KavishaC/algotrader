import yfinance as yf
import pandas as pd

def chart(ticker_symbol):
    # Define the ticker symbol of the stock you want data for
    """  if not is_valid_ticker(ticker_symbol):
        return {'ticker': ticker_symbol + ": Not valid Ticker", 'chart_data': []} """

    # Create a ticker object
    ticker = yf.Ticker(ticker_symbol)

    # Get historical data
    #historical_data = ticker.history(period="1d", interval="5m")  # You can specify the period ("1y", "5d", "max", etc.)
    #print("Company Name:", ticker.info['longName'])
    # Print the historical data
    for record in ticker.info:
        print(record, ": ", ticker.info[record])
        
    #historical_data.to_csv("historical_data.csv")

    # Print the result
    #chart_data = historical_data.reset_index().to_dict(orient='records')
    #print("chart info:", )
    #for record in chart_data:
        #record['x'] = pd.to_datetime(record['Datetime']).timestamp() * 1000  # Convert to milliseconds

        # Define the mapping function

    # Use the map function to apply the transformation to each element in the array
    #mapped_data = list(map(map_to_desired_format, chart_data))

    if 'currentPrice' in ticker.info:
        current_price = ticker.info['currentPrice']
    else:
        current_price = ticker.info['previousClose']
        
    # Calculate the percentage change
    close = ticker.info['previousClose']
    percentage_change = round(((current_price - close) / close) * 100, 2)
    if percentage_change > 0:
        status = "POSITIVE"
    elif percentage_change < 0:
        status = "NEGATIVE"
    elif percentage_change == 0:
        status = "ZERO"

    print("Percentage Change:")
    print(percentage_change)

    print("status:")
    print(status)
    # Create the final asset_sample dictionary
    asset_sample = {'ticker': ticker_symbol,
                    'longName': ticker.info['longName'],
                    'current_price': current_price,
                    'change': str(percentage_change) + "%",
                    'change_status': status,
                    'long_business_summary': ticker.info['longBusinessSummary'],}
    return asset_sample
    """'chart_data': mapped_data}"""

def chart_data(ticker_symbol, width):
    # Define the ticker symbol of the stock you want data for
    if not is_valid_ticker(ticker_symbol):
        return {'ticker': ticker_symbol + ": Not valid Ticker", 'chart_data': []}

    # Create a ticker object
    ticker = yf.Ticker(ticker_symbol)
    """ Valid intervals: [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo] """
    dateterm = "Date"
    if width=='oneD':
        period = '1d'
        interval = '2m'
        dateterm = "Datetime"
    elif(width=='oneW'):
        period = '1wk'
        interval = '15m'
        dateterm = "Datetime"
    elif(width=='oneM'):
        period = '1mo'
        interval = '90m'
        dateterm = "Datetime"
    elif(width=='threeM'):
        period = '3mo'
        interval = '1d'
    elif(width=='sixM'):
        period = '6mo'
        interval = '1d' 
    elif(width=='YTD'):
        period = '1y'
        interval = '1wk'
    elif(width=='oneY'):
        period = '1y'
        interval = '1wk'
    elif(width=='twoY'):
        period = '2y'
        interval = '1wk'
    elif(width=='fiveY'):
        period = '5y'
        interval = '1wk'
    elif(width=='tenY'):
        period = '10y'
        interval = '1mo'

    # Get historical data
    historical_data = ticker.history(period=period, interval=interval)  # You can specify the period ("1y", "5d", "max", etc.)
    #print("Company Name:", ticker.info['longName'])
    # Print the historical data
    """ for record in ticker.info:
        print(record, ": ", ticker.info[record]) """
        
    historical_data.to_csv("historical_data.csv")

    # Print the result
    chart_data = historical_data.reset_index().to_dict(orient='records')
    #print("chartData:", chart_data)
    for record in chart_data:
        record['x'] = pd.to_datetime(record[f"{dateterm}"]).timestamp() * 1000  # Convert to milliseconds

        # Define the mapping function

    # Use the map function to apply the transformation to each element in the array
    mapped_data = list(map(map_to_desired_format, chart_data))

    if 'currentPrice' in ticker.info:
        current_price = ticker.info['currentPrice']
    else:
        current_price = ticker.info['previousClose']
        
    # Calculate the percentage change
    close = ticker.info['previousClose']
    percentage_change = round(((current_price - close) / close) * 100, 2)
    if percentage_change > 0:
        status = "POSITIVE"
    elif percentage_change < 0:
        status = "NEGATIVE"
    elif percentage_change == 0:
        status = "ZERO"

    #print("Percentage Change:")
    #print(percentage_change)

    #print("status:")
    #print(status)
    # Create the final asset_sample dictionary
    asset_sample = {'ticker': ticker_symbol,
                    'longName': ticker.info['longName'],
                    'current_price': current_price,
                    'change': str(percentage_change) + "%",
                    'change_status': status,
                    'long_business_summary': ticker.info['longBusinessSummary'],
                     'chart_data': mapped_data}
    return {'chart_data': mapped_data}

def chart_sample():
    # Define the ticker symbol of the stock you want data for
    ticker_symbol = "AAPL"  # Example: Apple Inc.

    # Create a ticker object
    ticker = yf.Ticker(ticker_symbol)

    # Get historical data
    historical_data = ticker.history(period="3mo")  # You can specify the period ("1y", "5d", "max", etc.)

    # Print the historical data
    print(historical_data)
    historical_data.to_csv("historical_data.csv")

    chart_data = historical_data.reset_index().to_dict(orient='records')
    for record in chart_data:
        record['x'] = pd.to_datetime(record['Date']).timestamp() * 1000  # Convert to milliseconds

        # Define the mapping function

    # Use the map function to apply the transformation to each element in the array
    mapped_data = list(map(map_to_desired_format, chart_data))

    # Create the final asset_sample dictionary
    asset_sample = {'ticker': "AAPL", 'chart_data': mapped_data}
    return asset_sample

def is_valid_ticker(ticker_symbol):
    try:
        yf.Ticker(ticker_symbol).info
        return True
    except ValueError:
        return False
    
def map_to_desired_format(entry):
    return {
        'x': int(entry['x']),
        'o': round(entry['Open'], 2),
        'h': round(entry['High'], 2),
        'l': round(entry['Low'], 2),
        'c': round(entry['Close'], 2)
    }

def all_tickers():
    # Get all tickers
    all_tickers = yf.Tickers("all")

    # Print the list of all tickers
    print("All Tickers:", all_tickers.tickers)

#chart("AAPL")
#all_tickers()