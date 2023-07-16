# order_flow.py
# Order flow trading strategy. This strategy places a buy order when the order flow 
# imbalance exceeds a certain threshold, and places a sell order when the order flow imbalance is 
# below a certain threshold.

from exchanges.kucoin_helpers import KucoinTradingBot
from strategies.strategy import Strategy
from config import trading_variables as tv
import logging

class OrderFlow(Strategy):
    def __init__(self):
        super().__init__('Order Flow')

    def run(self, symbol, level2Data, features):
        
        # Calculate the order flow imbalance
        bids_volume = level2Data['total_bid_volume']
        asks_volume = level2Data['total_ask_volume']
        imbalance = (bids_volume - asks_volume) / (bids_volume + asks_volume)

        # Define the imbalance threshold
        imbalance_threshold = tv.imbalance_threshold

        # Check market condition
        market_condition = features['market_condition']

        # Place a limit order based on order flow imbalance and market condition
        if market_condition == 'high_volatility':
            if imbalance > imbalance_threshold:
                # Place a buy limit order at the best bid price
                best_bid = level2Data['bids'][0][0]             
                try:
                    KucoinTradingBot.create_buy_order(symbol, size=0.001, price=best_bid)
                except Exception as e:
                    logging.error(f"Failed to place buy order: {e}")
            
            elif imbalance < -imbalance_threshold:
                # Place a sell limit order at the best ask price
                best_ask = level2Data['asks'][0][0]
                try:
                    KucoinTradingBot.create_sell_order(symbol, size=0.001, price=best_ask)
                except Exception as e:
                    logging.error(f"Failed to place sell order: {e}")

        # Check the value of the `order_flow` feature
        order_flow = level2Data['order_flow']

        # If the order flow is positive, place a buy order
        if order_flow > 0:
            try:
                KucoinTradingBot.create_buy_order(symbol, size=0.001, price=best_bid)
            except Exception as e:
                logging.error(f"Failed to place buy order: {e}")

        # If the order flow is negative, place a sell order
        elif order_flow < 0:
            try:
                KucoinTradingBot.create_sell_order(symbol, size=0.001, price=best_ask)
            except Exception as e:
                logging.error(f"Failed to place sell order: {e}")
