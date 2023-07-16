import asyncio
import os
import sys
import time
import signal
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from stable_baselines3 import A2C, DDPG, PPO
from exchanges.kucoin_local import KucoinTrading
from exchanges.kucoin_helpers import KucoinTradingBot
from machine_learning import MachineLearning
from strategies.backtest import Backtest

from config import (
    csv_data,
    csv_base_path,
    monitor_performance as monitor_perf,
    perform_backtest,
    train_and_compare_models,
)

# Set up logging
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def train_models(csv_data_path):
    """
    Trains and compares machine learning models using the CSV data at csv_data_path.
    """
    try:
        ml = MachineLearning(csv_data_path)
        ml.train_and_compare_models()
    except FileNotFoundError:
        logging.error("Training data file not found.")
        sys.exit(1)

def monitor_performance():
    """
    Monitors the performance of the program and exits gracefully if a stop file is detected or 
    a keyboard interrupt is received.
    """
    def exit_handler(signum, frame):
        logging.info("Signal {} received. Exiting...".format(signum))
        sys.exit(1)

    signal.signal(signal.SIGINT, exit_handler)
    signal.signal(signal.SIGTERM, exit_handler)

    try:
        while True:
            if os.path.exists("stop.txt"):
                logging.info("Stop file detected. Exiting...")
                break
            time.sleep(60)
    except Exception as e:
        logging.error("Error occurred during monitoring: %s", str(e))
        sys.exit(1)

def main():
    """
    Main function that processes the CSV data at filenames and performs various tasks based on 
    the configuration in config.py.
    """
    try:
        for filename in csv_data:
            csv_data_path = os.path.join(csv_base_path, filename)
            logging.info("Processing file: %s", csv_data_path)

            ml = MachineLearning(csv_data_path)
            if train_and_compare_models:
                train_models(csv_data_path)

            if perform_backtest:
                Backtest.backtest_strategies()

        if monitor_perf:
            monitor_performance()

        # Add this line to start the Kucoin trading
        loop = asyncio.get_event_loop()
        loop.run_until_complete(KucoinTradingBot.main())
    except Exception as e:
        logging.info("An error occurred: %s", str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()

