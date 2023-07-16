from keras.models import load_model
import logging as logger
from exchanges.kucoin_helpers import KucoinTradingBot
from strategy import Strategy

class FiveMinuteScalper(Strategy):
    def __init__(self):
        super().__init__('Five Minute Scalper')

    def run(self, symbol, kline_feed, level2Data, features, model):
        try:
            logger.info(f"Executing 5 Minute Scalper for {symbol}")

            # Retrieve order book imbalance from level2Data
            order_book_imbalance = level2Data['order_imbalance'] if level2Data else None

            # Add order book imbalance to features
            features['order_book_imbalance'] = order_book_imbalance

            # Get the prediction from the model
            if kline_feed is not None:
                prediction = model.predict(kline_feed)
            else:
                logger.error("Kline feed is None")
                return

            momentum = features['momentum']
            historical_volatility = features['historical_volatility']
            market_condition = features['market_condition']

            # Calculate the amount to trade based on available balance
            bot = KucoinTradingBot()  # Assuming KucoinTradingBot is a class and you have appropriate constructor
            quantity = bot.calculate_allocation_amount() / kline_feed['close'].iloc[-1]

            if prediction > 0 and momentum > 0 and historical_volatility > 0.01 and market_condition == 'high_volatility':
                buying_price = bot.calculate_order_price(symbol, kline_feed['close'].iloc[-1], 'buy')
                logger.info(f"Buying {quantity} {symbol} at {buying_price}")
                bot.create_buy_order(symbol, quantity, buying_price)
            elif prediction < 0 and momentum < 0 and historical_volatility > 0.01 and market_condition == 'high_volatility':
                selling_price = bot.calculate_order_price(symbol, kline_feed['close'].iloc[-1], 'sell')
                logger.info(f"Selling {quantity} {symbol} at {selling_price}")
                bot.create_sell_order(symbol, quantity, selling_price)
        except Exception as e:
            logger.exception(f"Error executing strategy: {e}")
            return
