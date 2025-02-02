# Algorithmic Trading Bot

# This is the main file for implementing the trading bot's logic.

# Import necessary libraries for data manipulation, numerical calculations, and historical stock data retrieval
import pandas as pd  # Import pandas for data manipulation
import numpy as np  # Import numpy for numerical calculations
import yfinance as yf  # Import yfinance to fetch historical stock data
import logging  # Import logging for tracking events and performance

# Set up logging configuration to track events and performance at the INFO level
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to retrieve historical price data for a specified symbol and date range
def get_historical_data(symbol, start_date, end_date):
    # Use yfinance to download historical data for the specified symbol and date range
    data = yf.download(symbol, start=start_date, end=end_date)
    # Return the downloaded data
    return data  

# Function to handle NaN values in the historical data by filling them using the forward fill method
def handle_nan_values(data):
    # Fill NaN values using forward fill method
    data.fillna(method='ffill', inplace=True)  # Forward fill
    # Return the cleaned data
    return data  

# Function to calculate the moving average of a price series over a specified window
def calculate_moving_average(prices, window):
    # Calculate the moving average over the specified window
    return prices.rolling(window=window).mean()  # Return the moving average

# Function to generate buy/sell signals based on the price series and moving average
def generate_signals(prices, moving_average):
    # Create a signals series initialized with NaN
    signals = pd.Series(index=prices.index)
    # Set buy signal when price is below 98% of moving average
    signals[prices < moving_average * 0.98] = 1  
    # Set sell signal when price is above 102% of moving average
    signals[prices > moving_average * 1.02] = -1  
    # Return the signals
    return signals  

# Function to backtest the trading strategy using the price series and generated signals
def backtest_strategy(prices, signals):
    # Initialize starting capital for backtesting
    initial_capital = 10000  
    # Initialize shares owned
    shares = 0  
    # Initialize cash available
    cash = initial_capital  
    # List to track portfolio value over time
    portfolio_value = []  

    # Iterate over each date in the price series
    for date in prices.index:
        # Check if buy signal is generated
        if signals[date] == 1:  
            # Buy as many shares as possible
            shares += cash // prices[date]  
            # Deduct the cost from cash
            cash -= shares * prices[date]  
            # Log the buy action
            logging.info(f'Buying {shares} shares on {date} at {prices[date]}')  
        # Check if sell signal is generated and shares are owned
        elif signals[date] == -1 and shares > 0:  
            # Sell all shares
            cash += shares * prices[date]  
            # Log the sell action
            logging.info(f'Selling {shares} shares on {date} at {prices[date]}')  
            # Reset shares to zero
            shares = 0  
        # Calculate portfolio value
        portfolio_value.append(cash + shares * prices[date])  

    # Calculate final portfolio value
    final_value = cash + shares * prices[-1]  
    # Log final portfolio value
    logging.info(f'Final portfolio value: {final_value}')  
    # Return the final portfolio value
    return final_value  

# Main function to execute the trading bot
def main():
    # Indicate that the bot is starting
    print('Starting the Algorithmic Trading Bot...')  
    # Example symbol for Apple Inc.
    symbol = 'AAPL'  
    # Start date for historical data
    start_date = '2020-01-01'  
    # End date for historical data
    end_date = '2025-01-01'  
    # Fetch historical data
    historical_data = get_historical_data(symbol, start_date, end_date)  
    # Handle NaN values
    historical_data = handle_nan_values(historical_data)  
    # Calculate moving average
    moving_average = calculate_moving_average(historical_data['Close'], window=20)  
    # Generate trading signals
    signals = generate_signals(historical_data['Close'], moving_average)  
    # Backtest the strategy
    final_value = backtest_strategy(historical_data['Close'], signals)  
    # Print final portfolio value
    print(f'Final portfolio value after backtesting: {final_value}')  

# Run the main function if the script is executed directly
if __name__ == '__main__':
    main()  
