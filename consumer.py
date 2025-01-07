#neccesary headers for functions
import json

#must install with pip install kafka-python-ng
from kafka import KafkaConsumer

#must install with pip install pymongo
from pymongo import MongoClient

#connecting mongodb to the correct port
MONGO_URI = 'mongodb://localhost:27017/'
#Name of the database we are using
DATABASE_NAME = 'kafka_web_attack_data'
COLLECTION_NAME = 'consumer_records'

#Set up MongoDB Client
mongo_client = MongoClient(MONGO_URI)
#set up thje mongo database
db = mongo_client[DATABASE_NAME]
collection = db[COLLECTION_NAME] 

#Create a Kafka consumer instance with configuration
consumer = KafkaConsumer(
	#this is the kafaka topic to pull from
    'my_topic',
	api_version=(0,11,5),
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
	data = WebAttack.value
	#Insert data into MongoDB
	collection.insert_one(data)