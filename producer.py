#edited by Alec Ippolito and Max Benko
import csv
import json
import random
import time
from kafka import KafkaProducer

# Serializes the input data to a JSON-formatted string and encodes it to UTF-8 bytes. Note: Called implicitly via producer.send()
def json_serializer(data):
    return json.dumps(data).encode('utf-8')

# Open database and read content
with open('csic_database.csv', 'r') as file:
	csv_reader = csv.DictReader(file)
	rows = list(csv_reader)
	
# Kafka Topic and Producer Object Creation
topic = 'my_topic'
producer = KafkaProducer(
	api_version=(0,11,5),
    bootstrap_servers=['localhost:9092'],
    value_serializer=json_serializer,
	)

# Send Messages
for index, item in enumerate(rows):
	time.sleep(random.randint(1, 10)) 
	print(f"Sending Message {index}:\nProducer:\t{producer}\nTopic:\t\t{topic}\nContent:\t{item}\n")
	producer.send(topic, value=item) 
	producer.flush() # Ensure the message is sent immediatly

# Cleanup
print("Sending done...Cleanning up by closing producer!")
producer.close()