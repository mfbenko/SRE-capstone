#edited by Alec Ippolito and Max Benko
import csv
import json
import random
import time
from kafka import KafkaProducer

# Serializes the input data to a JSON-formatted string and encodes it to UTF-8 bytes. Note: Called implicitly via producer.send()
def json_serializer(data):
    return json.dumps(data).encode('utf-8')

class KafkaProducerService:
	def __init__(self):
		self.rows = ''
		self.topic = 'my_topic'
		self.producer = ''

	def create_producer(self,file='csic_database.csv'):
		# Open database and read content
		with open(file, 'r') as file:
			csv_reader = csv.DictReader(file)
			self.rows = list(csv_reader)
		
		# Kafka Topic and Producer Object Creation
		self.producer = KafkaProducer(
			api_version=(0,11,5),
			bootstrap_servers=['localhost:9092'],
			value_serializer=json_serializer,
			)
		return self.producer
	# Send Messages
	def send_message(self):
		for index, item in enumerate(self.rows):
			#time.sleep(random.randint(1, 10)) 
			print(f"Sending Message {index}:\nProducer:\t{self.producer}\nTopic:\t\t{self.topic}\nContent:\t{item}\n")
			self.producer.send(self.topic, value=item) 
			self.producer.flush() # Ensure the message is sent immediatly

		# Cleanup
		print("Sending done...Cleanning up by closing producer!")
		self.producer.close()

if __name__ == "__main__":
    producer_obj = KafkaProducerService()
    producer_obj.create_producer()
    producer_obj.send_message() 