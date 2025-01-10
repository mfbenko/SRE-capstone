#necessary imports to get pull information out of the database
from pymongo import MongoClient

#connecting mongodb to the correct port
client = MongoClient('mongodb://localhost:27017/')
#Name of the database we are using
db = client['kafka_web_attack_data']
#Name of the collection that messages are stored in
collection = db['consumer_records']

#returns all messages in the database(may change later)
results = collection.find()

#loop throught the dictionary we just created and print to the screen
for message in results:
    print(message)
	
#prepare data for insertion into mySQL by creating summary records
	
#we did it... stop the connection
client.close()