# Import necessary packages
from kafka import KafkaConsumer

TOPIC_NAME = 'user_profiles'

consumer = KafkaConsumer(TOPIC_NAME)

for message in consumer:
    print(message.value)