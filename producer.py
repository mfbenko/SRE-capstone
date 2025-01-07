#neccesary headers for functions
import csv
import json
import random
import time

#must install with pip install kafka-python-ng
from kafka import KafkaProducer

#open the database file with read only permision
with open('csic_database.csv', 'r') as file:
	#create reader object and begin reading one line at a time in loop and make each row a dictionary
	csv_reader = csv.DictReader(file)
	#create a list of dictionaries
	rows = list(csv_reader)
	
#return the json information as byte encoded
def json_serializer(data):
    return json.dumps(data).encode('utf-8')

#Create a Kafka producer instance with configuration
producer = KafkaProducer(
	#Address of the Kafka broker
    bootstrap_servers=['localhost:9092'],
	#set the serializer method to be the custom one we made
    value_serializer=json_serializer,
	)

#This is the kafka topic where the messages will be sent
topic = 'my_topic'

#begin the simulation with this loop
for item in rows:
	#generate a random number for simulation
	random_int = random.randint(1, 10)
	#sleep inorder to simulate real world randomness
	time.sleep(random_int)	
	#Convert an item in the list of dictionaries to JSON
	json_string = json.dumps(item, indent=4)
	#send the json item to the producer
	producer.send(topic, value=json_string)

#The messages have been sent...free up space
producer.close()