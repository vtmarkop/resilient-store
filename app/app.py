import os
import redis
from flask import Flask, jsonify

app = Flask(__name__)

# Connect to Redis. 
# 'redis-service' is the DNS name Kubernetes gives to the database.
# socket_connect_timeout=1 ensures we don't hang forever if DB is down.
r = redis.Redis(host='redis-service', port=6379, db=0, socket_connect_timeout=1)

@app.route('/buy', methods=['POST'])
def buy_item():
    try:
        # Try to decrement stock
        stock = r.decr('inventory')
        return jsonify({"message": "Purchase successful!", "stock_remaining": stock})
    except redis.exceptions.ConnectionError:
        # Graceful Error Handling: The App survives, even if the DB is dead.
        return jsonify({"error": "Store is temporarily offline (Database Down). Please try again."}), 503

@app.route('/reset', methods=['POST'])
def reset_stock():
    try:
        r.set('inventory', 100)
        return jsonify({"message": "Stock reset to 100"})
    except redis.exceptions.ConnectionError:
        return jsonify({"error": "Cannot reset stock (Database Down)"}), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)