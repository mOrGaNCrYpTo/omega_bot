#mean_reversion.py

from exchanges.kucoin_helpers import KucoinTradingBot
from strategies.strategy import Strategy
import logging as logger

class MeanReversionStrategy(Strategy):
    def __init__(self):
        super().__init__('Mean Reversion')

    def run(self, symbol, level2Data, features):
        
        logger.info(f"Executing Mean Reversion for {symbol}")
          
        # Get the last price
        last_price = features['price']

        # Calculate dynamic mean level and threshold
        mean = features['sma']
        threshold = features['std_dev']

        # Calculate the quantity to trade based on available balance
        quantity = KucoinTradingBot.calculate_allocation_amount() / last_price

        # Place a market order based on mean reversion
        if last_price > mean + threshold:
            best_bid = level2Data['bids'][0][0]
            KucoinTradingBot.create_sell_order(symbol, quantity, best_bid)
        elif last_price < mean - threshold:
            best_ask = level2Data['asks'][0][0]
            KucoinTradingBot.create_buy_order(symbol, quantity, best_ask)

