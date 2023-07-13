import redis
import mysql.connector
import json

# Redis connection
redis_host = 'localhost'
redis_port = 6379
redis_db = 0
redis_queue = 'event_queue'


def read_data_from_queue():
    redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
    data = redis_client.lrange(redis_queue, 0, -1)

    if data is not None:
        return data
    else:
        return None


# Usage


def insert_json_data(json_data):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mysql@123",
        database="Events",
        auth_plugin='mysql_native_password'
    )

    cursor = connection.cursor()
    query = f"INSERT INTO event_details (user_id, event_type, timestamp) VALUES ({json_data['user_id']}, " \
            f"'{json_data['event_type']}', '{json_data['timestamp']}');"

    print(query)
    cursor.execute(query)

    connection.commit()

    print("Data inserted successfully!")


if __name__ == "__main__":
    import json

    data = read_data_from_queue()
    if data is not None:
        print("Data read from redis_queue:", data)
    else:
        print("Queue is empty.")

    for index, record in enumerate(data):
        decoded_data = record.decode().replace("'", '"')
        record_dict = json.loads(decoded_data)
        print(f'{index}: {record_dict}')
        insert_json_data(record_dict)
