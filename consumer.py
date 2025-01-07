#neccesary headers for functions
import json

#must install with pip install kafka-python-ng
from kafka import KafkaConsumer


#Create a Kafka consumer instance with configuration
consumer = KafkaConsumer(
	#this is the kafaka topic to pull from
    'my_topic',
	#Address of the Kafka broker
    bootstrap_servers=['localhost:9092'],
	#first message in will be first message read
    auto_offset_reset='earliest', 
	#Automatically commit offsets after consuming messages
    enable_auto_commit=True,
	#Consumer group ID to allow multiple consumers to balance the load
    group_id='my-group',
	#switch from JSON objects to python objecets
    value_deserializer=lambda x: json.loads(x.decode('utf-8')) 
)

#begin consuming
print("Listening for messages...")
for WebAttack in consumer:
    #begin pymongo insertion into MongoDB
