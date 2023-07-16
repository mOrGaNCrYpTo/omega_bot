# kucoin.py

import asyncio
import logging
import pandas as pd

from kucoin.ws_token.token import GetToken
from kucoin.ws_client import KucoinWsClient

from strategies.fiveminutescalper import FiveMinuteScalper
from strategies.breakout import Breakout
from strategies.mean_reversion import MeanReversion
from strategies.order_flow import OrderFlow
from strategies.sma_crossover import SmaCrossover
from exchanges.kucoin_helpers import KucoinTradingBot

class KucoinTrading:
    def __init__(self):
        self.trading_bot = KucoinTradingBot()
        self.strategies = {
            'high_volatility': FiveMinuteScalper(),
            'trending_up': [Breakout(), SmaCrossover()],
            'trending_down': [Breakout(), SmaCrossover()],
            'range_bound': MeanReversion(),
        }

    async def deal_msg(self, msg):
        try:
            df = pd.DataFrame(msg["data"])
            features = self.trading_bot.get_features(df)
            level2Data = self.trading_bot.get_level2Data(df)
            symbol = msg['subject'].split(':')[1]

            market_condition = features['market_condition']
            strategies = self.strategies.get(market_condition)

            if strategies is not None:
                if isinstance(strategies, list):
                    for strategy in strategies:
                        strategy.run(symbol, features, level2Data)
                else:
                    strategies.run(symbol, features, level2Data)
            else:
                logging.info('Market condition is not defined')

            OrderFlow().run(symbol, features, level2Data)
        except Exception as e:
            logging.error('An error occurred while dealing with the message: %s', e)

async def main():
    trading = KucoinTrading()

    # Define the client once, depending on which API you want to use
    token_client = GetToken()   
    ws_client = await KucoinWsClient.create(None, token_client, trading.deal_msg, private=False)

    await ws_client.subscribe('/market/ticker:BTC-USDT,ETH-BTC,SOL-BTC')
    await ws_client.subscribe('/spotMarket/level2Depth5:BTC-USDT,ETH-BTC,SOL-BTC')

    while True:
        await asyncio.sleep(60)  # Use only the `sleep` function, no need to specify the loop parameter

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
