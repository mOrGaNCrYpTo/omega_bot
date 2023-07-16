import config
import pyodbc

conn_str = config.sql_connection_string

class MsSql:
    def __init__(self, conn_str):
        self.conn_str = conn_str

    def save_trade(self, trade):
        with pyodbc.connect(self.conn_str) as conn:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO Trades (symbol, side, price, fee, quantity, time, exchange) VALUES (?, ?, ?, ?, ?, ?, ?)",
                            trade['symbol'], trade['side'], trade['price'], trade['fee'], trade['quantity'], trade['time'], trade['exchange'])
                conn.commit()

    def get_trades(self, symbol, start_date, end_date):
        with pyodbc.connect(self.conn_str) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM Trades WHERE symbol = ? AND time >= ? AND time <= ?", symbol, start_date, end_date)
                trades = cursor.fetchall()
        return trades

    def get_all_trades(self):
        with pyodbc.connect(self.conn_str) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM Trades")
                trades = cursor.fetchall()
        return trades

    def get_trade_by_id(self, id):
        with pyodbc.connect(self.conn_str) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM Trades WHERE id = ?", id)
                trade = cursor.fetchone()
        return trade

    def update_trade(self, trade):
        with pyodbc.connect(self.conn_str) as conn:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE Trades SET symbol = ?, side = ?, price = ?, fee = ?, quantity = ?, time = ?, exchange = ? WHERE id = ?",
                            trade['symbol'], trade['side'], trade['price'], trade['fee'], trade['quantity'], trade['time'], trade['exchange'], trade['id'])
                conn.commit()

    def delete_trade(self, id):
        with pyodbc.connect(self.conn_str) as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM Trades WHERE id = ?", id)
                conn.commit()

    def get_profit_and_loss(self, symbol, start_date, end_date):
        with pyodbc.connect(self.conn_str) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT SUM(price * quantity) as total FROM Trades WHERE symbol = ? AND time >= ? AND time <= ? AND side = 'sell'",
                            symbol, start_date, end_date)
                total_sell = cursor.fetchone()
                cursor.execute("SELECT SUM(price * quantity) as total FROM Trades WHERE symbol = ? AND time >= ? AND time <= ? AND side = 'buy'",
                            symbol, start_date, end_date)
                total_buy = cursor.fetchone()
        return (total_sell[0] if total_sell else 0) - (total_buy[0] if total_buy else 0)

    def get_total_traded_volume(self, symbol, start_date, end_date):
        with pyodbc.connect(self.conn_str) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT SUM(quantity) as total FROM Trades WHERE symbol = ? AND time >= ? AND time <= ?", symbol, start_date, end_date)
                total = cursor.fetchone()
        return total[0] if total else 0

