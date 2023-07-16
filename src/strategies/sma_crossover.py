from exchanges.kucoin_helpers import KucoinTradingBot
from strategies.strategy import Strategy
from pyalgotrade.technical import cross
import logging as logger
import numpy as np

class SmaCrossover(Strategy):
    def __init__(self, short_period, long_period):
        super().__init__('SMA Crossover')

    def run(self, symbol, level2Data, features):
        
        # Calculate short and long SMA
        short_sma = features['short_sma']
        long_sma = features['long_sma']
        
        # Check if the SMAs crossed
        golden_cross = cross.cross_above(short_sma.values, long_sma.values)
        death_cross = cross.cross_below(short_sma.values, long_sma.values)

        # Check if level2Data is not None
        if level2Data:
            best_bid = level2Data['bids'][0][0]
            best_ask = level2Data['asks'][0][0]
        else:
            logger.error("Level2Data is None")
            return

        if np.any(golden_cross):  # golden cross
            try:
                KucoinTradingBot.create_buy_order(symbol, size=0.001, price=best_bid)
            except Exception as e:
                logger.error(f"Failed to place buy order: {e}")

        elif np.any(death_cross):  # death cross
            try:
                KucoinTradingBot.create_sell_order(symbol, size=0.001, price=best_ask)
            except Exception as e:
                logger.error(f"Failed to place sell order: {e}")
