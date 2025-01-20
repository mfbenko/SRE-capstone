#edited by Alec Ippolito and Max Benko
import csv
import json
import random
import time
from kafka import KafkaProducer

class producer:
	def __init__(self):
		self.rows = ''
		self.topic = 'my_topic'

	# Serializes the input data to a JSON-formatted string and encodes it to UTF-8 bytes. Note: Called implicitly via producer.send()
	def json_serializer(data):
		return json.dumps(data).encode('utf-8')

	def create_producer():
		# Open database and read content
		with open('csic_database.csv', 'r') as file:
			csv_reader = csv.DictReader(file)
			self.rows = list(csv_reader)
		
		# Kafka Topic and Producer Object Creation
		producer = KafkaProducer(
			api_version=(0,11,5),
			bootstrap_servers=['localhost:9092'],
			value_serializer=json_serializer,
			)

	# Send Messages
	def send_message():
		for index, item in enumerate(self.rows):
			time.sleep(random.randint(1, 10)) 
			print(f"Sending Message {index}:\nProducer:\t{producer}\nTopic:\t\t{self.topic}\nContent:\t{item}\n")
			producer.send(self.topic, value=item) 
			producer.flush() # Ensure the message is sent immediatly

		# Cleanup
		print("Sending done...Cleanning up by closing producer!")
		producer.close()