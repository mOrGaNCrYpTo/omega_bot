import logging
import os
from kucoin_account import KucoinAccount

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set up the KuCoin account
api_key = os.getenv("KUCOIN_API_KEY")
api_secret = os.getenv("KUCOIN_API_SECRET")
api_passphrase = os.getenv("KUCOIN_API_PASSPHRASE")

def monitor_performance():
    try:
        # Initialize KuCoin helper classes
        account_client = KucoinAccount(api_key, api_secret, api_passphrase)
        
        trades = account_client.getTrades()
        
        # Initialize metrics
        total_profit = 0
        winning_trades = 0
        losing_trades = 0
        profits = []

        # Calculate metrics
        for trade in trades:
            profit = trade['profit']
            total_profit += profit
            profits.append(profit)
            if profit > 0:
                winning_trades += 1
            elif profit < 0:
                losing_trades += 1

        # Calculate additional metrics
        total_trades = winning_trades + losing_trades
        win_rate = winning_trades / total_trades if total_trades > 0 else 0
        average_profit = total_profit / total_trades if total_trades > 0 else 0
        max_drawdown = min(profits) if profits else 0

        logging.info(f"Total trades: {total_trades}, Winning trades: {winning_trades}, Losing trades: {losing_trades}")

        # Return metrics
        return {
            'total_profit': total_profit,
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': win_rate,
            'average_profit': average_profit,
            'max_drawdown': max_drawdown,
        }
    except Exception as e:
        logging.error(f"An error occurred while monitoring performance: {e}")
        return None
