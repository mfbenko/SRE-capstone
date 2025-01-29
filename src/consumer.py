import asyncio
import json
from kafka import KafkaConsumer
from pymongo import MongoClient

class KafkaConsumerService:
    def __init__(self, topic, bootstrap_servers, mongo_uri, database_name, collection_name, logger=None):
        # Define MongoDB Constants
        self.mongo_uri = mongo_uri
        self.database_name = database_name
        self.collection_name = collection_name
        self.logger = logger

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
            self.logger.info(f"\n\033[92mReceived message:\033[0m {json.dumps(data, indent=4)}") if self.logger is not None else None
            yield data

    # Method to insert data into MongoDB Collection
    def insert_into_mongodb(self, data):
        try:
            self.collection.insert_one(data)
            self.logger.info(f"Inserted data into MongoDB: {data}") if self.logger is not None else None
        except Exception as e:
            self.logger.error(f"Error inserting data into MongoDB: {e}") if self.logger is not None else None
        
    # Method to start the consumer, consumer message, and insert into MongoDB
    async def run(self):
            loop = asyncio.get_event_loop()
            for message_data in self.consume_messages():
                try:
                    await loop.run_in_executor(None, self.insert_into_mongodb, message_data) 
                except Exception as e:
                    self.logger.error(f"Error processing message: {e}")