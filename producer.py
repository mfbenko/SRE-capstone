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
    
    def read_database(self, file):
        # Open database and read content
        with open(file, 'r') as file:
            self.logger.info(f"File {file} created successfully.") if self.logger is not None else None
            csv_reader = csv.DictReader(file)
            self.rows = list(csv_reader)
        random.shuffle(self.rows) 

    def create_producer(self, file):
        self.read_database(file)
        # Kafka Topic and Producer Object Creation
        self.producer = KafkaProducer(
            api_version=(0,11,5),
            bootstrap_servers=['localhost:9092'],
            value_serializer=self.json_serializer,
        )
        self.logger.info("Producer created successfully.") if self.logger is not None else None

    # Send Messages
    def send_message(self):
        for index, item in enumerate(self.rows):
            time.sleep(1) 
            if item[''] == "Normal" or item[''] == "Anomalous":
                self.logger.info(f"\n\033[94mSending Message {index}:\033[0m {json.dumps(item, indent=4)}") if self.logger is not None else None
                self.producer.send(self.topic, value=item) 
                self.producer.flush() # Ensure the message is sent immediately
                self.logger.info(f"Message {index} sent successfully.") if self.logger is not None else None
            if self.limit == index:
                break

        self.logger.info(f"Sending completed.") if self.logger is not None else None