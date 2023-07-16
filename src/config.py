# config.py

debug = True

sql_database = {
    "host": "localhost",
    "port": 5432,
    "username": "admin",
    "password": "admin",
    "database": "myapp_db",
}

sql_connection_string = "Driver={SQL Server};Server=HP\MFSQL;Database=TradeMonkey;Trusted_Connection=yes;"

redis_cache = {
    "port": 6379
}

train_and_compare_models = True
perform_backtest = True
monitor_performance = False

csv_base_path = 'D:\Repos\Omega_Bot\omega_bot\omega_bot\data'
csv_data = ['BTC-USDT.csv','ETH-BTC.csv','XRP-BTC.csv']

trading_variables = {
    'kucoin_transaction_fee': 0.08,
    'compounding_percentage': 0.5,
    'percentage_of_capital_to_trade': 0.3,
    'max_margin': 0.1,
    'risk_reward_multiple': 3,
    'stop_loss_percentage': 0.10,
    'atr_multiplier': 3,
    'rsi_Period': 14,
    'atr_Period': 14,
    'aroon_Period': 14,
    'bbands_Period': 20,
    'bbands_StdDev': 20,
    'macd_Fast': 12,
    'macd_Slow': 26,
    'macd_Signal': 9,
    'imbalance_threshold': 0.6,
    'window_size': 100,
    'trading_fee': 0.008,
    'slippage': 0.001,
    'short_sma': 50,
    'long_sma': 200
}