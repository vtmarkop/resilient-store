import os
import redis
import time
import signal
from flask import Flask, jsonify

app = Flask(__name__)

# Standard Redis connection (We keep the settings, but we don't trust them anymore)
r = redis.Redis(
    host='redis-service', 
    port=6379, 
    socket_connect_timeout=0.1, 
    socket_timeout=0.1, 
    retry_on_timeout=False
)

# Define a custom error for our alarm
class HardTimeoutError(Exception):
    pass

# The function that runs when the alarm rings
def handler(signum, frame):
    raise HardTimeoutError("Hard Deadline Exceeded")

@app.route('/buy', methods=['POST'])
def buy_item():
    start_time = time.time()
    
    # 1. Set the Alarm for 0.5 seconds (The Hard Limit)
    signal.signal(signal.SIGALRM, handler)
    signal.setitimer(signal.ITIMER_REAL, 0.5)
    
    try:
        # 2. Try the dangerous operation
        print(f"--- Attempting Purchase at {start_time} ---", flush=True)
        stock = r.decr('inventory')
        
        # 3. If successful, Disable the Alarm
        signal.setitimer(signal.ITIMER_REAL, 0)
        
        return jsonify({"message": "Purchase successful!", "stock_remaining": stock})

    except HardTimeoutError:
        # This catches OUR alarm
        duration = time.time() - start_time
        return jsonify({"error": f"CONSISTENT FAIL: Hard Timeout triggered. Waited {duration:.4f}s"}), 503

    except Exception as e:
        # This catches any other random error (like the 32s TCP fail if it happens fast enough)
        signal.setitimer(signal.ITIMER_REAL, 0) # Ensure alarm is off
        duration = time.time() - start_time
        return jsonify({"error": f"FAIL: {str(e)}. Waited {duration:.4f}s"}), 503

if __name__ == '__main__':
    # threaded=False is REQUIRED for signal to work
    app.run(host='0.0.0.0', port=5000, threaded=False)