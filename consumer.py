#edited by Alec Ippolito and Max Benko
import json
from kafka import KafkaConsumer
from pymongo import MongoClient

# # Define MongoDB Constants
# MONGO_URI = 'mongodb://localhost:27017/' # MongoDB Port
# DATABASE_NAME = 'kafka_web_attack_data'
# COLLECTION_NAME = 'consumer_records'

# # MongoDB Client
# mongo_client = MongoClient(MONGO_URI)
# db = mongo_client[DATABASE_NAME]
# collection = db[COLLECTION_NAME] 

# # Kafka Topic and Consumer Object Creation
# topic = 'my_topic'
# consumer = KafkaConsumer(
#     topic,
# 	api_version=(0,11,5),
#     bootstrap_servers=['localhost:9092'], # Kafka Broker
#     auto_offset_reset='earliest', 
#     enable_auto_commit=True,
#     group_id='my-group',
#     value_deserializer=lambda x: json.loads(x.decode('utf-8')) 
# )

# # Extract data from broker and insert it into MongoDB
# for WebAttack in consumer:
# 	data = WebAttack.value
# 	print(f"Recieving Data:\t\t{data}\n")
# 	collection.insert_one(data)



class KafkaConsumerService:
    def __init__(self, topic, bootstrap_servers, mongo_uri, database_name, collection_name):
            # Define MongoDB Constants
            self.mongo_uri = mongo_uri
            self.database_name = database_name
            self.collection_name = collection_name

            # MongoDB Client Creation
            self.mongo_client = MongoClient(self.mongo_uri)
            self.db = self.mongo_client[self.database_name]
            self.collection = self.db[self.collection_name]

            # Define Consumer Constants
            self.topic = topic
            self.bootstrap_servers = bootstrap_servers

            # Kafka Consumer Object Creation
            self.consumer = KafkaConsumer(
                self.topic,
                api_version=(0, 11, 5),
                bootstrap_servers=self.bootstrap_servers,
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                group_id='my-group',
                value_deserializer=lambda x: json.loads(x.decode('utf-8'))
            )

    # Method to Consume Message from the Kafka Topic
    def consume_messages(self):
        for message in self.consumer:
            data = message.value
            #print(f"Receiving Data:\t\t{data}\n")
            yield data

    # Method to insert data into MongoDB Collection
    def insert_into_mongodb(self, data):
        self.collection.insert_one(data)
        return True

    # Method to start the consumer, consumer message, and insert into MongoDB
    def run(self):
        for message_data in self.consume_messages():
            self.insert_into_mongodb(message_data)
        return True

if __name__ == "__main__":
    kafka_topic = 'my_topic'
    kafka_brokers = ['localhost:9092'] 
    mongo_uri = 'mongodb://localhost:27017/'
    mongo_db = 'kafka_web_attack_data'
    mongo_collection = 'consumer_records'
    consumer = KafkaConsumerService(
        kafka_topic, 
        kafka_brokers, 
        mongo_uri, 
        mongo_db, 
        mongo_collection
    )
    consumer.run()