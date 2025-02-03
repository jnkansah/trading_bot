# Algorithmic Trading Bot

This project aims to create an algorithmic trading bot to enhance quant applications. The bot implements a Mean Reversion Strategy with advanced risk management features.

## Project Structure
- `main.py`: Contains the main logic for the trading bot, including data retrieval, signal generation, and backtesting.
- `README.md`: Provides an overview of the project and its purpose.
- `requirements.txt`: Lists the dependencies required for the project.

## Features
- Fetches historical price data from Yahoo Finance using the `yfinance` library
- Implements a Mean Reversion Strategy based on moving averages
- Advanced risk management features:
  - Position sizing based on volatility
  - Stop-loss orders (2% threshold)
  - Sharpe ratio calculation for risk-adjusted returns
- Handles missing data using forward fill
- Backtests the trading strategy and logs trading actions

## Risk Management
The bot includes several risk management features:
1. **Position Sizing**: Dynamically adjusts position sizes based on market volatility
   - Higher volatility leads to smaller positions
   - Maximum position size is capped at 20% of portfolio value
2. **Stop-Loss Orders**: Automatically exits positions if losses exceed 2%
3. **Sharpe Ratio**: Measures risk-adjusted returns relative to the risk-free rate

## Installation
1. Clone the repository
2. Navigate to the project directory
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
- Optimize strategy parameters (moving average window, thresholds)
- Add more technical indicators
- Implement portfolio diversification
- Add real-time market data integration
- Enhance visualization of trading performance
- Add more sophisticated risk management techniques
