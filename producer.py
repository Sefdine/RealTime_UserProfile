import time
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
import requests
import json
import logging
import sys

# Set up logging
logging.basicConfig(level=logging.ERROR)

# Define the topic name
TOPIC_NAME = 'user_profiles'
# Define server name
SERVER_NAME = 'localhost:9092'

# Initialize the Kafka producer
try:
    producer = KafkaProducer(bootstrap_servers=SERVER_NAME, value_serializer=lambda v: json.dumps(v).encode('utf-8'))
except NoBrokersAvailable as ne:
    logging.error('No brokers available: %s', ne)
    sys.exit(1)

users = []

while len(users) < 100:
    try:
        # Fetch data from randomuser.me
        response = requests.get('https://randomuser.me/api/')

        # Send data if status code is good
        if response.status_code == 200:
            data = response.json()['results'][0]
            producer.send(TOPIC_NAME, value=data)
            producer.flush()

            print(f"User n°{len(users)+1} sent successfully!")

            users.append(data)

    except NoBrokersAvailable as ne:
        logging.error('No brokers available: %s', ne)
        break

    except Exception as e:
        logging.error('Error: %s', e)
        break

# Close the producer after sending all messages
producer.close()
