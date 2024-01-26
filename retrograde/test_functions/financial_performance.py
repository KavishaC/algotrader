import pandas as pd
import numpy as np
from datetime import datetime

# Your provided data
portfolio_data = [
    {
        "date": "2023-07-23",
        "cash": 1055.5632247924805,
        "assets": [
            {"ticker": "AAPL", "units": 21, "price": 191.42897033691406},
            {"ticker": "DJIA", "units": 30, "price": 21.638153076171875},
            {"ticker": "NKE", "units": 5, "price": 108.3307113647461},
            {"ticker": "AGG", "units": 2, "price": 96.35093688964844},
            {"ticker": "GC=F", "units": 1, "price": 1964.300048828125},
        ],
        "value": 8423.371673583984,
    },
    # ... other data entries
]

def generate_performance_data(portfolio_data):

    # Convert the data to a DataFrame for easier analysis
    df = pd.DataFrame(portfolio_data)
    df['date'] = pd.to_datetime(df['date'])

    # Calculate daily returns
    df['daily_returns'] = df['value'].pct_change()

    # Calculate portfolio cumulative returns
    df['cumulative_returns'] = (1 + df['daily_returns']).cumprod() - 1

    # Calculate daily log returns for volatility calculation
    df['log_returns'] = np.log(1 + df['daily_returns'])

    # Calculate volatility
    volatility = df['log_returns'].std() * np.sqrt(252)  # Assuming 252 trading days in a year

    # Assuming risk-free rate for Sharpe Ratio calculation
    risk_free_rate = 0.02  # Replace with the actual risk-free rate

    # Calculate Total Return
    total_return = (df['value'].iloc[-1] / df['value'].iloc[0]) - 1

    # Calculate Sharpe Ratio
    sharpe_ratio = (total_return - risk_free_rate) / volatility

    # Calculate Beta
    # For simplicity, let's assume DJIA as the benchmark
    benchmark_data = pd.DataFrame(portfolio_data)[['date', 'daily_returns']]
    benchmark_data = benchmark_data.rename(columns={'daily_returns': 'benchmark_returns'})
    merged_df = pd.merge(df, benchmark_data, on='date', how='left')
    cov_matrix = np.cov(merged_df['log_returns'].dropna(), merged_df['benchmark_returns'].dropna())
    beta = cov_matrix[0, 1] / np.var(merged_df['benchmark_returns'].dropna())

    # Calculate Alpha
    alpha = total_return - (risk_free_rate + beta * (benchmark_data['daily_returns'].mean() - risk_free_rate))

    # Calculate Treynor Ratio
    treynor_ratio = (total_return - risk_free_rate) / beta

    # Information Ratio, Drawdown Analysis, Yield and Income Metrics, Duration, Convexity
    # These metrics may require additional information and calculations specific to your portfolio and strategy

    # Display the calculated metrics
    print(f"Total Return: {total_return:.4f}")
    print(f"Sharpe Ratio: {sharpe_ratio:.4f}")
    print(f"Beta: {beta:.4f}")
    print(f"Alpha: {alpha:.4f}")
    print(f"Treynor Ratio: {treynor_ratio:.4f}")
    print(f"Volatility: {volatility:.4f}")

    return {
        total_return: "{total_return:.4f}",
        sharpe_ratio: "{sharpe_ratio:.4f}",
        beta: "{beta:.4f}",
        alpha: "{alpha:.4f}",
        treynor_ratio: "{treynor_ratio:.4f}",
        volatility: "{volatility:.4f}",
    }