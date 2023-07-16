# backtest.py

import argparse
import logging
import pandas as pd
import sys
import os

from strategies import Breakout
from strategies import MeanReversion
from strategies import TrendFollowing
from strategies import SMACrossover
from strategies import OrderFlow
from strategies import FiveMinuteScalper
from pyalgotrade import plotter

# Set up the logging level and format
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
  
class Backtest:
    def __init__(self, symbol, level2_Data, features, model, csv_data_path):
        self.symbol = symbol
        self.level2Data = level2_Data
        self.features = features
        self.model = model
        self.csv_data_path = csv_data_path
        self.data = pd.read_csv(csv_data_path)

def backtest_strategies(self):
    """
    Runs a series of backtests on different trading strategies.
    """
    try:
        strategies = [Breakout(), MeanReversion(), TrendFollowing(), SMACrossover(), OrderFlow()]
        for strategy in strategies:
            strategy.run(self.symbol, self.level2Data, self.features, self.model)
    except ImportError:
        logging.error("Strategy module not found.")
        sys.exit(1)
    except Exception as e:
        logging.error("Error occurred during backtest: %s", str(e))

# backtest_breakout_strategy
def backtest_breakout(self, symbol, level2Data, features, model):
    try:
        # Create the strategy
        strategy = Breakout()

        # Run the strategy
        strategy.run(symbol, level2Data, features, model)

        # Plot the results
        plt = plotter.StrategyPlotter(strategy)
        plt.plot()

    except Exception as e:
        logging.error("An error occurred: %s", str(e))
        sys.exit(1)

# backtest_fiveminutescalper
def backtest_fiveminutescalper(symbol, level2Data, features, model):
    try:
        # Create the strategy
        strategy = FiveMinuteScalper(symbol, level2Data, features, model)

        # Run the strategy
        strategy.run()

        # Plot the results
        plt = plotter.StrategyPlotter(strategy)
        plt.plot()

    except Exception as e:
        logging.error("An error occurred: %s", str(e))
        sys.exit(1)

# backtest_mean_reversion
def backtest_mean_reversion(symbol, level2Data, features):
    try:
        # Create the strategy
        strategy = MeanReversion(symbol, level2Data, features)

        # Run the strategy
        strategy.run()

        # Plot the results
        plt = plotter.StrategyPlotter(strategy)
        plt.plot()

    except Exception as e:
        logging.error("An error occurred: %s", str(e))
        sys.exit(1)

# backtest_sma_crossover
def backtest_sma_crossover(symbol, level2Data, features):
    try:
        # Create the strategy
        strategy = SMACrossover(symbol, level2Data, features)

        # Run the strategy
        strategy.run()

        # Plot the results
        plt = plotter.StrategyPlotter(strategy)
        plt.plot()

    except Exception as e:
        logging.error("An error occurred: %s", str(e))
        sys.exit(1)
        
# backtest_order_flow
def backtest_order_flow(symbol, level2Data, features):
    try:
        # Create the strategy
        strat = OrderFlow(symbol, level2Data, features)

        # Run the strategy
        strat.run()

        # Plot the results
        plt = plotter.StrategyPlotter(strat)
        plt.plot()

    except Exception as e:
        logging.error("An error occurred: %s", str(e))
        sys.exit(1)

def main():
    # Define the command-line arguments
    parser = argparse.ArgumentParser(description="Backtest different trading strategies on KuCoin")

    parser.add_argument("-s", "--symbol", type=str, required=True, help="The trading symbol to backtest on")

    parser.add_argument("-sd", "--start_date", type=str, required=True, help="The start date of the backtesting period in YYYY-MM-DD format")

    parser.add_argument("-ed", "--end_date", type=str, required=True, help="The end date of the backtesting period in YYYY-MM-DD format")

    parser.add_argument("-q", "--quantity", type=float, required=True, help="The quantity of the asset to trade in each transaction")

    parser.add_argument("-st", "--strategy", type=str, required=True, choices=["fiveminutescalper", "trend_following", "mean_reversion"], help="The strategy to backtest")

    parser.add_argument("-fp", "--file_path", type=str, default=None, help="The file path of the CSV data for fiveminutescalper strategy")

    parser.add_argument("-mp", "--model_path", type=str, default=None, help="The file path of the ANN model for fiveminutescalper strategy")
    
    # Parse the command-line arguments
    args = parser.parse_args()
    
    if args.file_path is None or args.model_path is None:
        raise ValueError("You need to provide both file_path and model_path")
    else:      
        
        # Trading configuration
        window_size=100
        trading_fee=0.008
        slippage=0.001
        
        df = pd.read_csv ('file_name.csv')
        
        KucoinTradingBot = KucoinTradingBot()
        features = KucoinTradingBot.get_features(df)
        
        # Call the corresponding backtesting function based on the strategy argument
        if args.strategy == "fiveminutescalper":
            backtest_fiveminutescalper(args.file_path, args.model_path)
                    
        elif args.strategy == "mean_reversion":
            backtest_mean_reversion(args.symbol, args.start_date, args.end_date, args.quantity)
        
        elif args.strategy == "breakout":
            backtest_breakout(args.symbol, args.start_date, args.end_date, args.quantity)
            
        elif args.strategy == "smacrossover":
            backtest_sma_crossover(args.symbol, args.start_date, args.end_date, args.quantity)
            
        elif args.strategy == "orderflow":
            backtest_order_flow(args.symbol, args.start_date, args.end_date, args.quantity)
                
    def preprocess_data(self):
        self.data['datetime'] = pd.to_datetime(self.data['openTime'])
        self.data.set_index('datetime', inplace=True)
        self.data['target'] = self.data['closePrice'].shift(-1)
        self.data.dropna(inplace=True)

        # Sort the DataFrame by the index (datetime)
        self.data = self.data.sort_index()

        # Now drop the unnecessary columns
        self.X = self.data.drop(columns=['symbol', 'openTime', 'target'])

        # Convert y to a 1D array
        self.y = np.array(self.data['target']).ravel()
        
if __name__ == "__main__":
    # Run the main function
    main()