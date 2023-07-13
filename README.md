# Jumbotail_assignment2

1.Event producer:
This code represents an event producer that generates events and sends them to a webhook URL using concurrent threads. The events are randomly selected from a predefined event list.

This contains a driver class which uses concurrent threads to generate and send events for multiple users.
- The event_producer class has '__init__' method that initializes the object for the weburl parameter.This URL acts as endpoints where all these events will be sent.
- 
- The EventProducer class is defined with an __init__ method and two other methods: generate_event and send_event.
-The  generate._event method which will generate the events of the users like "access_app", "click_banner", "view_products", "select_product", "add_to_cart","place_order" with a unique user_id and returns the events in json format and each event contains user_id,event_type and timestamp.
-The sent_event method which will send the events to specified URL using request.post function.
-The logging module is used to log the events and errors to a file.

2.webhook and memory queue:
This code represents simple Flaskapi that receives incoming events through a webhook and pushes them to an in-memory queue using Redis. 
-An instance of the flask application is created with the name app.

-A connection to redis is established using redis.Redis().
-The '/webhook' route is denfined and it expects a incoming post request.When a request is received the event data is extracted from the JOSN data payload and passed it through the push_to_queue() function.
-The push_to_queue function takes an event parameter and is responsible for pushing the event to the Redis queue. It configures the connection details, including the host, port, and database of the Redis server.
-Within in this function a retry mechanism is implemented to handle potential failuers while pushing the event to the queue.
-It uses a while loop and retries the operation a maximum number of times (max_retry_attempts). If an exception is raised during the push operation, the function waits for a specified duration (retry_delay_seconds) before retrying. If the maximum number of retries is reached, an error message is printed.
-In the main section the Flask application is set to run on 'localhost' with port '8888'.

3.Queue consumer and Database:
This code reads data from redis queue and inserting the JSON data into MySQL database.

-Redis connection details are defined, including the host, port, database, and queue name.
-The read_data_from_queue function establishes a connection to Redis using the provided connection details.It retrives all the data drom the redis queue using lrange command.If data doesn't exists in the queue it will return None.
-The insert_json_data function takes JSON data as input and inserts it into a MySQL database. It establishes a connection to the MySQL server using the provided connection details like host,user,password,database name.
-It creates a SQL query to insert the data into the event_details table and executes the query using a cursor.The connection is committed to persist the changes.
-In the main section, the read_data_from_queue function is called to retrieve data from the Redis queue. If data exists, it is printed; otherwise, a message indicating an empty queue is printed.
-Each record in the retrieved data is decoded, converted to a dictionary using json.loads, and passed to the insert_json_data function for insertion into the MySQL database.



## Table of Contents

- [Installation](#installation)
- Before using this project, ensure that you have the following prerequisites:
Python 3.7 or higher
Pip package manager
Redis
MySQL workbench




- [Usage](#usage)


1.Clone the repository:

git clone https://github.com/Sharandeep02/Jumbotail_assignment2

2.Navigate to the project directory:

cd your-project

3.Install the required dependencies:

pip install -r requirements.txt

update redis_host,redis_port,redis_db,redis_queue 
update  host=" ",user=" ",password=" ",database=" " in read_data.py file


Getting Started
To start the project, run the following command:

first run - webhook.py file this file runs the flask api which we created.And this accepts the payload.

Next run event_producer.py this python file will generate the events and send it to the flask api

Next run read_data.py this python file will  read data from redis queue and inserting the JSON data into MySQL database.





