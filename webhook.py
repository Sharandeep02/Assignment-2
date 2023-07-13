import time
from flask import Flask, request
import redis

app = Flask(__name__)
# Connect to the Redis server
r = redis.Redis()


@app.route('/webhook', methods=['POST'])
def webhook():
    event = request.json
    push_to_queue(event)
    return 'Event received and queued.'


def push_to_queue(event):
    # Push event to the in-memory queue (Redis)
    # Implement retry mechanism if push operation fails
    # Push the event to the queue
    # Create the queue
    redis_host = 'localhost'
    redis_port = 6379
    redis_db = 0
    redis_queue = 'event_queue'

    # Retry configuration
    max_retry_attempts = 3
    retry_delay_seconds = 1
    retry_count = 0
    redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
    print(event)
    event = str(event)
    while retry_count < max_retry_attempts:
        try:
            redis_client.rpush(redis_queue, event)
            print("Event pushed to queue successfully")
            return
        except redis.exceptions.RedisError as e:
            print(f"Pushing event to queue failed: {str(e)}")
            retry_count += 1
            time.sleep(retry_delay_seconds)
    print("redis success")
    print("Max retry attempts reached. Failed to push event to queue.")


if __name__ == '__main__':
    app.run(host='localhost', port=8888)
