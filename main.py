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
    data.fillna(method='ffill', inplace=True)
    return data

# Function to calculate volatility over a specified window
def calculate_volatility(prices, window=20):
    # Calculate daily returns
    returns = prices.pct_change()
    # Calculate rolling standard deviation of returns
    volatility = returns.rolling(window=window).std()
    return volatility

# Function to calculate position size based on volatility
def calculate_position_size(cash, price, volatility, max_position_size=0.2, target_volatility=0.02):
    # Adjust position size inversely to volatility
    if volatility == 0:
        return 0
    position_size = min(cash * max_position_size / price, 
                       cash * (target_volatility / volatility) / price)
    return int(position_size)

# Function to calculate the moving average of a price series over a specified window
def calculate_moving_average(prices, window):
    # Calculate the moving average over the specified window
    return prices.rolling(window=window).mean()

# Function to generate buy/sell signals based on the price series and moving average
def generate_signals(prices, moving_average):
    # Create a signals series initialized with NaN
    signals = pd.Series(index=prices.index)
    # Set buy signal when price is below 98% of moving average
    signals[prices < moving_average * 0.98] = 1
    # Set sell signal when price is above 102% of moving average
    signals[prices > moving_average * 1.02] = -1
    return signals

# Function to calculate the Sharpe ratio of the strategy
def calculate_sharpe_ratio(portfolio_values, risk_free_rate=0.05):
    # Convert portfolio values to returns
    portfolio_returns = pd.Series(portfolio_values).pct_change().dropna()
    
    # Calculate excess returns (returns above risk-free rate)
    # Convert annual risk-free rate to daily
    daily_rf_rate = (1 + risk_free_rate) ** (1/252) - 1
    excess_returns = portfolio_returns - daily_rf_rate
    
    # Calculate annualized Sharpe ratio
    # Multiply by sqrt(252) to annualize (252 trading days)
    sharpe_ratio = np.sqrt(252) * (excess_returns.mean() / excess_returns.std())
    
    return sharpe_ratio

# Function to backtest the trading strategy using the price series and generated signals
def backtest_strategy(prices, signals):
    # Initialize starting capital for backtesting
    initial_capital = 10000
    # Initialize shares owned
    shares = 0
    # Initialize cash available
    cash = initial_capital
    # List to track portfolio value over time
    portfolio_values = []
    
    # Calculate volatility for position sizing
    volatility = calculate_volatility(prices)
    
    # Stop-loss parameters
    stop_loss_pct = 0.02  # 2% stop loss
    entry_price = None
    
    # Iterate over each date in the price series
    for date in prices.index:
        current_price = prices[date]
        
        # Check stop-loss if we have a position
        if shares > 0 and entry_price is not None:
            loss_pct = (current_price - entry_price) / entry_price
            if loss_pct < -stop_loss_pct:
                # Trigger stop-loss
                cash += shares * current_price
                logging.info(f'Stop-loss triggered: Selling {shares} shares on {date} at {current_price}')
                shares = 0
                entry_price = None
        
        # Generate trading signals
        if signals[date] == 1 and shares == 0:  # Buy signal
            # Calculate position size based on volatility
            position_size = calculate_position_size(cash, current_price, volatility[date])
            if position_size > 0:
                shares = position_size
                cash -= shares * current_price
                entry_price = current_price
                logging.info(f'Buying {shares} shares on {date} at {current_price}')
        
        elif signals[date] == -1 and shares > 0:  # Sell signal
            cash += shares * current_price
            logging.info(f'Selling {shares} shares on {date} at {current_price}')
            shares = 0
            entry_price = None
        
        # Calculate and store portfolio value for this day
        current_value = cash + shares * current_price
        portfolio_values.append(current_value)
    
    # Calculate final portfolio value
    final_value = cash + shares * prices.iloc[-1]
    
    # Calculate Sharpe ratio
    sharpe_ratio = calculate_sharpe_ratio(portfolio_values)
    logging.info(f'Strategy Sharpe Ratio: {sharpe_ratio:.2f}')
    
    return final_value, sharpe_ratio, portfolio_values

def main():
    print('Starting the Algorithmic Trading Bot...')
    symbol = 'AAPL'
    start_date = '2020-01-01'
    end_date = '2025-01-01'
    
    historical_data = get_historical_data(symbol, start_date, end_date)
    historical_data = handle_nan_values(historical_data)
    moving_average = calculate_moving_average(historical_data['Close'], window=20)
    signals = generate_signals(historical_data['Close'], moving_average)
    
    # Unpack the returned values from backtest_strategy
    final_value, sharpe_ratio, portfolio_values = backtest_strategy(historical_data['Close'], signals)
    
    print(f'Final portfolio value after backtesting: ${final_value:,.2f}')
    print(f'Strategy Sharpe Ratio: {sharpe_ratio:.2f}')

# Run the main function if the script is executed directly
if __name__ == '__main__':
    main()
