import string
from prompt_toolkit import prompt
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def moving_average_crossover_strategy(stock_data):
    # Calculate the 50-day and 200-day simple moving averages
    stock_data['SMA_50'] = stock_data['Close'].rolling(window=50).mean()
    stock_data['SMA_200'] = stock_data['Close'].rolling(window=200).mean()

    # Create Buy and Sell signals based on crossovers
    stock_data['Signal'] = 0
    stock_data.loc[stock_data['SMA_50'] > stock_data['SMA_200'], 'Signal'] = 1
    stock_data.loc[stock_data['SMA_50'] < stock_data['SMA_200'], 'Signal'] = -1

    return stock_data

# Get the list of S&P 500 symbols from a CSV file or any other source
# For demonstration purposes, I'll use a static list of example symbols here.
sp500_symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'GOOGL', 'META', 'GOOG', 'JPM', 'JNJ']

# List to temp store results
results_list = []
symbols_to_buy = []

start = (input('Enter the start date to analyize data: Format Required: 2023-01-01: \n'))
end = (input('Enter the end date to analyize data: Format Required: 2023-01-01: \n'))

# Loop through each stock symbol in the S&P 500 list
for symbol in sp500_symbols:
    try:
        # Download historical data for the stock
        stock_data = yf.download(symbol, start=start, end=end)
        
        
        # Apply the moving average crossover strategy
        stock_data = moving_average_crossover_strategy(stock_data)
        # Append the results to the overall DataFrame
        latest_data = stock_data.iloc[-1]
        # print('latest_data[-1]', latest_data[-1])
        if (latest_data[-1]==1):
            symbols_to_buy.append(symbol)
        # results_df = results_df.append(latest_data)  # Save the last row (latest data) of each stock
        results_list.append(latest_data)  # Save the last row (latest data) of each stock
        #results_df = pd.concat([results_df, pd.DataFrame([latest_data])], ignore_index=True)
        # print('results_list', results_list)
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")

# Create DataFrame to store the results
results_df = pd.DataFrame(results_list)

# Filter the results to show only stocks with a buy signal
buy_signals_df = results_df[results_df['Signal'] == 1]

# Display the list of stocks with buy signals
print('Stocks to Buy:', symbols_to_buy)
print("Stocks with Buy Signals:")
print(buy_signals_df[['Open', 'Close', 'SMA_50', 'SMA_200']])

# Stock to by index tracker:
stb_index = 0

# Optionally, you can plot the charts for each stock with buy signals
for index, row in buy_signals_df.iterrows():
    stock_symbol = symbols_to_buy[stb_index]
    stb_index += 1
    # print(stock_symbol)
    stock_data = yf.download(stock_symbol, start=start, end=end)
    stock_data = moving_average_crossover_strategy(stock_data)
    
    plt.figure(figsize=(12, 6))
    plt.plot(stock_data.index, stock_data['Close'], label='Close Price', color='blue')
    plt.plot(stock_data.index, stock_data['SMA_50'], label='50-day SMA', color='orange')
    plt.plot(stock_data.index, stock_data['SMA_200'], label='200-day SMA', color='red')
    plt.scatter(index, row['Close'], s=100, marker='^', color='g', label='Buy Signal')
    
    plt.title(f'{stock_symbol} - Moving Average Crossover Strategy')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()
    