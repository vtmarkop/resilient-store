import os
import redis
from flask import Flask, jsonify

app = Flask(__name__)

# Connect to Redis. 
# 'redis-service' is the DNS name Kubernetes gives to the database.
# socket_connect_timeout=1 ensures we don't hang forever if DB is down.
#r = redis.Redis(host='redis-service', port=6379, db=0, socket_connect_timeout=1) 
#r = redis.Redis(host='redis-service', port=6379, db=0, socket_connect_timeout=1, socket_timeout=1)

# socket_timeout=0.1  -->  If no answer in 100ms, hang up.
# retry_on_timeout=False --> Do NOT try again. Fail immediately.
r = redis.Redis(host='redis-service', port=6379, db=0, socket_connect_timeout=0.1, socket_timeout=0.1, retry_on_timeout=False)

@app.route('/buy', methods=['POST'])
def buy_item():
    import time
    start_time = time.time()
    print(f"--- Attempting Purchase at {start_time} ---", flush=True)

    try:
        # Try to decrement stock
        stock = r.decr('inventory')
        return jsonify({"message": "Purchase successful!", "stock_remaining": stock})

    except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError) as e:
        end_time = time.time()
        duration = end_time - start_time
        print(f"!!! FAILED after {duration:.2f} seconds. Error: {e} !!!", flush=True)
        
        return jsonify({"error": f"FAST FAIL: Store is temporarily offline. Waited {duration:.2f}s"}), 503

@app.route('/reset', methods=['POST'])
def reset_stock():
    try:
        r.set('inventory', 100)
        return jsonify({"message": "Stock reset to 100"})
    except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError):
        return jsonify({"error": "Cannot reset stock (Database Down)"}), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)