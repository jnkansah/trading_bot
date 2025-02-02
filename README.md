# Algorithmic Trading Bot

This project aims to create an algorithmic trading bot to enhance quant applications. The bot implements a Mean Reversion Strategy and provides insights into trading performance.

## Project Structure
- `main.py`: Contains the main logic for the trading bot, including data retrieval, signal generation, and backtesting.
- `README.md`: Provides an overview of the project and its purpose.
- `requirements.txt`: Lists the dependencies required for the project.

## Features
- Fetches historical price data from Yahoo Finance using the `yfinance` library.
- Implements a Mean Reversion Strategy based on moving averages.
- Handles missing data using forward fill.
- Backtests the trading strategy and logs trading actions and final portfolio value.

## Installation
1. Clone the repository.
2. Navigate to the project directory.
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the trading bot by executing the following command:
```bash
python main.py
```

## Future Work
- Optimize the trading strategy parameters.
- Implement risk management features.
- Visualize trading performance over time.
- Integrate with a live trading platform for real-time trading.
