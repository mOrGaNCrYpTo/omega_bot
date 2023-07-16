import redis
import json

# redis_client = RedisClient()
# redis_client.save_trade(some_trade)
# retrieved_trade = redis_client.get_trade(some_trade_id)
# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

class RedisClient:
    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.Redis(host=host, port=port, db=db)

    def save_trade(self, trade):
        # Convert the trade to a JSON string
        trade_json = json.dumps(trade)

        # Save the trade in Redis, using the trade ID as the key
        self.client.set(trade['id'], trade_json)

    def get_trade(self, trade_id):
        # Get the trade from Redis
        trade_json = self.client.get(trade_id)

        # Convert the JSON string back to a dictionary
        trade = json.loads(trade_json)

        return trade
    
    def delete_trade(self, trade_id):
        self.client.delete(trade_id)
        
    def get_all_trades(self):
        trade_ids = self.client.keys()
        trades = [self.get_trade(trade_id) for trade_id in trade_ids]
        return trades

    def get_open_orders(self, symbol):
        pass
        
    def flush_db(self):
        self.client.flushdb()
        
    def save_data(self, key, data, expiration_in_seconds):
        # Convert the data to a JSON string
        data_json = json.dumps(data)

        # Save the data in Redis with an expiration time
        self.client.setex(key, expiration_in_seconds, data_json)

    def get_data(self, key):
        # Get the data from Redis
        data_json = self.client.get(key)

        # Convert the JSON string back to a dictionary
        if data_json is not None:
            data = json.loads(data_json)
            return data
        else:
            return None

# USAGE
# # Initialize the Redis client
# redis_client = RedisClient()

# # Save some WebSocket data with a 60-second expiration time
# websocket_data = {"price": 100.0, "volume": 200.0}  # Replace with your actual WebSocket data
# redis_client.save_data('websocket_data', websocket_data, 60)

# # Get the WebSocket data
# retrieved_data = redis_client.get_data('websocket_data')
# print(retrieved_data)

