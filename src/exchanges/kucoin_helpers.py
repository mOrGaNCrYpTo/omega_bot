# kucoin_helpers.py
# This file contains helper functions for the Kucoin exchange.

import numpy as np
import talib
import logging
import os
import pandas as pd
import data.ms_sql as db
from config import trading_variables as tv
from kucoin.client import Market
from kucoin.client import Trade
from kucoin.client import Account

class KucoinTradingBot:
    def __init__(self):
        # Load Kucoin API credentials
        self.api_key = os.getenv("KUCOIN_API_KEY")
        self.api_secret = os.getenv("KUCOIN_API_SECRET")
        self.api_passphrase = os.getenv("KUCOIN_API_PASSPHRASE")
        
        # Load trading variables
        self.transaction_fee = tv['kucoin_transaction_fee']
        self.compounding_percentage = tv['compounding_percentage']
        self.percentage_of_capital_to_trade = tv['percentage_of_capital_to_trade']
        self.max_margin = tv['max_margin']
        self.risk_reward_multiple = tv['risk_reward_multiple']
        self.stop_loss_percentage = tv['stop_loss_percentage']
        
        # Instantiate Kucoin clients
        self.kucoin_orders_client = Trade(self.api_key, self.api_secret, self.api_passphrase)
        self.kucoin_account_client = Account(self.api_key, self.api_secret, self.api_passphrase)
        self.kucoin_data_client = Market(self.api_key, self.api_secret, self.api_passphrase)
        
    def get_features(feed):
        # config
        rsiPeriod = tv.rsi_Period
        atrPeriod = tv.atr_Period
        aroonPeriod = tv.aroon_Period
        bbandsPeriod = tv.bbands_Period
        bbandsStdDev = tv.bbands_StdDev
        macdFast = tv.macd_Fast
        macdSlow = tv.macd_Slow
        macdSignal = tv.macd_Signal
        
        # Calculate the technical indicators
        ema10 = talib.EMA(feed['close'], timeperiod=10)
        ema30 = talib.EMA(feed['close'], timeperiod=30)
        ema50 = talib.EMA(feed['close'], timeperiod=50)
        ema100 = talib.EMA(feed['close'], timeperiod=100)
        ema200 = talib.EMA(feed['close'], timeperiod=200)
        
        # Calculate short and long SMA
        short_sma = talib.SMA(feed['close'], timeperiod=tv.short_sma)
        long_sma = talib.SMA(feed['close'], timeperiod=tv.long_sma)

        # Calculate VWAP
        typical_price = (feed['high'] + feed['low'] + feed['close']) / 3
        vwap = sum(typical_price * feed['volume']) / sum(feed['volume'])

        # Calculate Momentum
        momentum = feed['close'] - feed['close'].shift(10)  # Here, we use 10 periods momentum. You can adjust this number as needed.

        # Calculate historical volatility
        returns = feed['close'].pct_change()
        historical_volatility = returns.rolling(window=10).std() * np.sqrt(252)  # Here we use 10-day historical volatility. Adjust the window as needed.

        # Bollinger bands
        bb_bands = talib.BollingerBands(feed['close'], period= bbandsPeriod, numStdDev=bbandsStdDev)

        # Bollinger Bands again. Do I need both?
        upper_band, middle_band, lower_band = talib.BBANDS(feed['close'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)

        # RSI        
        rsi = talib.RSI(feed['close'], timeperiod=rsiPeriod)

        # ATR
        atr = talib.ATR(feed['high'], feed['low'], feed['close'], timeperiod=atrPeriod)

        # MACD
        macd = talib.MACD(feed['close'], fastperiod=macdFast, slowperiod=macdSlow, signalperiod=macdSignal)

        # AARON
        aroonosc = talib.AROON(feed['high'], feed['low'], timeperiod=aroonPeriod, indicator='aroonosc')

        # Calculate the ATR value
        atr = talib.ATR(feed['high'], feed['low'], feed['close'], timeperiod=atrPeriod)[-1]

        # Check if the EMAs are crossed
        long_position = ema50[-1] > ema100[-1]
        short_position = ema50[-1] < ema100[-1]

        # Check for bullish and bearish divergences
        bullish_divergence = rsi[-1] > 50 and macd[-1] > macd[-2] and rsi[-1] < rsi[-2]
        bearish_divergence = rsi[-1] < 50 and macd[-1] < macd[-2] and rsi[-1] > rsi[-2]

        # Check if the price is within the Bollinger Bands
        out_of_band = feed['close'] > bb_bands.getUpperBand()[-1] or feed['close'] < bb_bands.getLowerBand()[-1]

        # Calculate order flow
        order_flow = feed['volume'].diff()  # The difference in volume from the previous period

        # Check if the price is above or below support and resistance
        support = feed['1h_low'].min()
        resistance = feed['1h_high'].max()
        above_resistance = feed['close'] > resistance
        below_resistance = feed['close'] < resistance
        below_support = feed['close'] < support

        # Calculate a signal strength factor based on the MACD and RSI
        signal_strength = (macd[-1] / macd.getMax()) * 0.5 + (rsi[-1] / rsi.getMax()) * 0.5

        # Determine the stop loss level based on the ATR value
        if long_position:
            stop_loss = feed['close'] - (2 * atr)
        elif short_position:
            stop_loss = feed['close'] + (2 * atr)
        else:
            stop_loss = None
            
        # Determine market condition based on indicator values
        market_condition = get_market_condition(feed)

        # Create a DataFrame with the features
        features = pd.DataFrame({
            'symbol': feed['symbol'],
            'price': feed['close'],
            'last4prices': feed['close'].rolling(4).mean(),
            'ema10': ema10,
            'ema30': ema30,
            'ema50': ema50,
            'ema100': ema100,
            'ema200': ema200,
            'vwap': vwap,
            'momentum': momentum,
            'historical_volatility': historical_volatility,
            'rsi': rsi,
            'atr': atr,
            'macd': macd,
            'long_position': long_position,
            'shortPos': short_position,
            'bullish_divergence': bullish_divergence,
            'bearish_divergence': bearish_divergence,
            'upper_band': upper_band,
            'middle_band': middle_band,
            'lower_band': lower_band,
            'out_of_band': out_of_band,
            'support': support,
            'resistance': resistance,
            'above_resistance': above_resistance,
            'below_resistance': below_resistance,
            'below_support': below_support,
            'signal_strength': signal_strength,
            'stop_loss': stop_loss,
            'market_condition': market_condition,
            'order_flow': order_flow,
            'short_sma': short_sma,
            'long_sma': long_sma
        })
            
        # Return the features as a numpy array
        return features.values[-1].reshape(1, -1)

def get_level2Data(level2_feed):
    bids = level2_feed['bids']
    asks = level2_feed['asks']
    total_bid_volume = sum(bid[1] for bid in bids)
    total_ask_volume = sum(ask[1] for ask in asks)
    weighted_bid_price = sum(bid[0] * bid[1] for bid in bids) / total_bid_volume
    weighted_ask_price = sum(ask[0] * ask[1] for ask in asks) / total_ask_volume
    order_imbalance = level2_feed['total_bid_volume'] - level2_feed['total_ask_volume']
    return {
        'bids': bids,
        'asks': asks,
        'total_bid_volume': total_bid_volume,
        
        'total_ask_volume': total_ask_volume,
        'weighted_bid_price': weighted_bid_price,
        'weighted_ask_price': weighted_ask_price,
        'order_imbalance': order_imbalance,
    }
    
def get_market_condition(feed):
    # Calculate the technical indicators
    ema50 = talib.EMA(feed['close'], timeperiod=50)
    ema100 = talib.EMA(feed['close'], timeperiod=100)
    rsi = talib.RSI(feed['close'], timeperiod=14)
    bb_bands = talib.BollingerBands(feed['close'], period=20, numStdDev=2)
    atr = talib.ATR(feed['high'], feed['low'], feed['close'], timeperiod=14)
    volume = feed['volume']
    
    # Determine market condition based on indicator values
    if rsi > 70:
        market_condition = 'bullish'
    elif rsi < 30:
        market_condition = 'bearish'
    elif ema50[-1] > ema100[-1]:
        market_condition = 'trending_up'
    elif ema50[-1] < ema100[-1]:
        market_condition = 'trending_down'
    elif feed['close'] > bb_bands.getUpperBand()[-1] or feed['close'] < bb_bands.getLowerBand()[-1]:
        market_condition = 'range_bound'
    elif atr > feed['close'] * 0.01:
        market_condition = 'high_volatility'
    elif atr < feed['close'] * 0.005:
        market_condition = 'low_volatility'
    elif volume < 10000:
        market_condition = 'low_volume'
    else:
        market_condition = 'sideways'
        
    return market_condition

def get_ticker(symbol):
    ticker = KucoinData.get_ticker(symbol)
    return float(ticker['price'])

def calculate_order_price(current_price, order_type):
    if order_type == 'buy':
        return current_price - (current_price * 0.01) # Buy slightly below the current price
    elif order_type == 'sell':
        return current_price + (current_price * 0.01) # Sell slightly above the current price

def create_buy_order(symbol, price):
    # Fetch current price and determine the buying price
    buying_price = calculate_order_price(price, 'buy')

    # Calculate the quantity to trade based on available balance
    allocation_amount = calculate_allocation_amount()
    quantity = allocation_amount / buying_price

    # Create a market buy order
    buy_order = KucoinOrders.create_market_order(symbol, 'buy', quantity=quantity, price=buying_price)

    # Save the trade to the database
    db.save_trade(symbol, 'buy', quantity, buying_price, buy_order['orderId'])

    logging.info('Buy order placed: %s', buy_order)

def create_sell_order(symbol, price):
    # Fetch current price and determine the selling price
    selling_price = calculate_order_price(price, 'sell')

    # Calculate the quantity to trade based on available balance
    allocation_amount = calculate_allocation_amount()
    quantity = allocation_amount / selling_price

    # Create a limit sell order
    sell_order = KucoinOrders.create_limit_order(symbol, 'sell', price=selling_price, size=quantity)

    # Save the trade to the database
    db.save_trade(symbol, 'sell', quantity, selling_price, sell_order['orderId'])

    logging.info('Sell order placed: %s', sell_order)

def get_available_balance():
    account_info = KucoinAccount.getAccountInfo()
    return float(account_info['balances']['USDT']['available'])

def get_order(order_id):
    order = KucoinOrders.get_order_info(order_id)
    return order

def get_orders(self, order_ids):
    orders = []
    for order_id in order_ids:
        order = self.kucoin_orders_client.get_orders(order_id)
        orders.append(order)
    return orders

#Set purchases to be 3% of your available equity
def calculate_allocation_amount():
    available_balance = get_available_balance()
    allocation_amount = available_balance * tv.percentage_of_capital_to_trade  
    return allocation_amount

def calculate_take_profit_price(current_price, stop_loss_price):
    return current_price + (current_price - stop_loss_price) * tv.risk_reward_multiple

def calculate_stop_loss_price(self, current_price, atr, atr_multiplier=1):
    return current_price - (atr * atr_multiplier)

