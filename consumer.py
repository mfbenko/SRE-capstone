#edited by Alec Ippolito and Max Benko
import json
from kafka import KafkaConsumer
from pymongo import MongoClient

# Define MongoDB Constants
MONGO_URI = 'mongodb://localhost:27017/' # MongoDB Port
DATABASE_NAME = 'kafka_web_attack_data'
COLLECTION_NAME = 'consumer_records'

# MongoDB Client
mongo_client = MongoClient(MONGO_URI)
db = mongo_client[DATABASE_NAME]
collection = db[COLLECTION_NAME] 

# Kafka Topic and Consumer Object Creation
topic = 'my_topic'
consumer = KafkaConsumer(
    topic,
	api_version=(0,11,5),
    bootstrap_servers=['localhost:9092'], # Kafka Broker
    auto_offset_reset='earliest', 
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')) 
)

# Extract data from broker and insert it into MongoDB
for WebAttack in consumer:
	data = WebAttack.value
	print(f"Recieving Data:\t\t{data}\n")
	collection.insert_one(data)
