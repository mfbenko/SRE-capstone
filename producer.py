#edited by Alec Ippolito and Max Benko
#neccesary headers for functions
import csv
import json
import random
import time

#must install with pip install kafka-python-ng
from kafka import KafkaProducer

#open the csv database file with read only permision
with open('csic_database.csv', 'r') as file:
	#create reader object and begin reading one line at a time in loop and make each row a dictionary
	csv_reader = csv.DictReader(file)
	#create a list of dictionaries
	rows = list(csv_reader)
	
#function to convert Python dictionaries to JSON. Called implicitly via producer.send()
def json_serializer(data):
	#kafka only accepts byte encoded JSON
    return json.dumps(data).encode('utf-8')

#Create a Kafka producer instance with configuration
producer = KafkaProducer(
	#speicify which API version we will be using
	api_version=(0,11,5),
	#Port of the Kafka broker
    bootstrap_servers=['localhost:9092'],
	#set the serializer method to be the custom one we made
    value_serializer=json_serializer,
	)

#This is the kafka topic where the messages will be sent
topic = 'my_topic'

print("sending messages...")
#begin the simulation with this loop
for item in rows:
	#generate a random number for simulation
	random_int = random.randint(1, 10)
	#sleep inorder to simulate real world randomness
	time.sleep(random_int)	
	#send the item to the producer after serialization
	producer.send(topic, value=item)
#The messages have been sent...free up space
producer.close()