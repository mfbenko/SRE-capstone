import csv
import json
import random
import time
from kafka import KafkaProducer
import json

class KafkaProducerService:
    def __init__(self,logger=None, limit=None):
        self.rows = ''
        self.topic = 'my_topic'
        self.producer = None
        self.logger = logger
        self.limit = limit

    # Serializes the input data to a JSON-formatted string and encodes it to UTF-8 bytes. Note: Called implicitly via producer.send()
    @staticmethod
    def json_serializer(data):
        return json.dumps(data).encode('utf-8')

    def create_producer(self,file='csic_database.csv'):
        # Open database and read content
        with open(file, 'r') as file:
            self.logger.info(f"File {file} created successfully.")
            csv_reader = csv.DictReader(file)
            self.rows = list(csv_reader)
        
        # Kafka Topic and Producer Object Creation
        self.producer = KafkaProducer(
            api_version=(0,11,5),
            bootstrap_servers=['localhost:9092'],
            value_serializer=self.json_serializer,
        )
        self.logger.info("Producer created successfully.")

    # Send Messages
    def send_message(self):
        for index, item in enumerate(self.rows):
            time.sleep(random.randint(1, 10)) 
            if item[''] == "Normal" or item[''] == "Anomalous":
                self.logger.info(f"\n\033[94mSending Message {index}:\033[0m {json.dumps(item, indent=4)}")
                self.producer.send(self.topic, value=item) 
                self.producer.flush() # Ensure the message is sent immediately
                self.logger.info(f"Message {index} sent successfully.")
            if self.limit == index and self.index is not None:
                break

        self.logger.info(f"Sending completed.") 