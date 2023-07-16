import logging as logger
from exchanges.kucoin_helpers import KucoinTradingBot
from strategy import Strategy

class Breakout(Strategy):
    def __init__(self):
        super().__init__('Breakout')

    def run(self, symbol, level2Data, features, model):

        logger.info(f"Executing Breakout strategy for {symbol}")
        
        try:            
            # Get the prediction from the model
            model.predict(features)
            
            # Calculate the amount to trade based on available balance
            quantity = self.calculate_allocation_amount() / features['price']

            if features['price'] > features['resistance'] and features['momentum'] > 0 and features['historical_volatility'] > 0.01 and features['market_condition'] == 'trending_up':
                if level2Data and level2Data['bids']:
                    best_bid = min(level2Data['bids'], key=lambda x: x[0])
                    buying_price = self.calculate_order_price(best_bid[0], 'buy')
                else:
                    buying_price = features['price']  # Use current price if level2 data is not available
                self.create_buy_order(symbol, quantity, buying_price)

            elif features['price'] < features['support'] and features['momentum'] < 0 and features['historical_volatility'] > 0.01 and features['market_condition'] == 'trending_down':
                if level2Data and level2Data['asks']:
                    best_ask = max(level2Data['asks'], key=lambda x: x[0])
                    selling_price = self.calculate_order_price(best_ask[0], 'sell')
                else:
                    selling_price = features['price']  # Use current price if level2 data is not available
                self.create_sell_order(symbol, quantity, selling_price)

        except Exception as e:
            logger.error('An error occurred while executing the strategy: %s', e)
            raise e

