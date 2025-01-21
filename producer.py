#edited by Alec Ippolito and Max Benko
import csv
import json
import random
import time
from kafka import KafkaProducer

class KafkaProducerService:
	def __init__(self):
		self.rows = ''
		self.topic = 'my_topic'
		self.producer = None

	# Serializes the input data to a JSON-formatted string and encodes it to UTF-8 bytes. Note: Called implicitly via producer.send()
	@staticmethod
	def json_serializer(data):
		return json.dumps(data).encode('utf-8')

	def create_producer(self,file='csic_database.csv'):
		# Open database and read content
		with open(file, 'r') as file:
			csv_reader = csv.DictReader(file)
			self.rows = list(csv_reader)
		
		# Kafka Topic and Producer Object Creation
		self.producer = KafkaProducer(
			api_version=(0,11,5),
			bootstrap_servers=['localhost:9092'],
			value_serializer=self.json_serializer,
			)

	# Send Messages
	def send_message(self):
		for index, item in enumerate(self.rows):
			#time.sleep(random.randint(1, 10)) 
			if item[''] == "Normal" or item[''] == "Anomalous":
				print(f"Sending Message {index}:\nProducer:\t{self.producer}\nTopic:\t\t{self.topic}\nContent:\t{item}\n")
				self.producer.send(self.topic, value=item) 
				self.producer.flush() # Ensure the message is sent immediatly
			
		# Cleanup
		print("Sending done...Cleanning up by closing producer!")

if __name__ == "__main__":
    producer_obj = KafkaProducerService()
    producer_obj.create_producer()
    producer_obj.send_message() 