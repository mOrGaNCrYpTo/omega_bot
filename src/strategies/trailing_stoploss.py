# trailing_stoploss.py
# Implements a trailing stop loss strategy. This strategy places a buy order and a sell order at the same time.

# How should I use this to modify take profits to prevent losses and missed opportunities?

import time
import os
import logging
from config import trading_variables as tv
from exchanges.kucoin_helpers import KucoinTradingBot
from strategies.strategy import Strategy
from data import RedisClient

class TrailingStopLoss(Strategy):
    def __init__(self, short_period, long_period):
        super().__init__('SMA Crossover')
        self.short_period = short_period
        self.long_period = long_period

    def run(self, symbol, level2Data, features, model):
        try:
            allocation_amount = KucoinTradingBot.calculate_allocation_amount()
            
            if allocation_amount > 0:
                open_orders = RedisClient.get_open_order(symbol)
                
                if open_orders:
                    # Increase the quantity of the existing buy order
                    existing_order = open_orders[0]
                    existing_quantity = float(existing_order['size'])
                    new_quantity = existing_quantity + allocation_amount
                    KucoinTradingBot.edit_order(existing_order['id'], new_quantity=new_quantity)

                else:
                    # Create a new buy order
                    quantity = allocation_amount * tv.compounding_percentage
                    KucoinTradingBot.create_buy_order(symbol, quantity)

                # Monitor price movements and adjust stop loss level accordingly
                while True:
                    current_price = KucoinTradingBot.get_current_price(symbol)
                    stop_loss_level = current_price - current_price * tv.stop_loss_percentage
                    take_profit_level = current_price + current_price * tv.take_profit_percentage
                    
                    if current_price <= stop_loss_level:
                        KucoinTradingBot.create_sell_order(symbol, quantity)
                        break
                    elif current_price >= take_profit_level:
                        KucoinTradingBot.create_sell_order(symbol, quantity)
                        break

                    time.sleep(tv.monitoring_interval)  # Adjust the waiting period as per your trading strategy

        except Exception as e:
            logging.error('An error occurred: %s', str(e))