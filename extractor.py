#necessary import to get pull information out of the database
from pymongo import MongoClient

#pandas will be used so that we can make summary records
import pandas

#connecting mongodb to the correct port
client = MongoClient('mongodb://localhost:27017/')
#Name of the database we are using
db = client['kafka_web_attack_data']
#Name of the collection that messages are stored in
collection = db['consumer_records']

#returns all messages in the database(may change later)
results = collection.find()
#take the results and put them into a pandas dataframe(table)
pandasTable = pandas.DataFrame(results)
	
#prepare data for insertion into mySQL by creating summary records.
#we will group data by normal/anomalous(represented by '') and http method
summary_record = pandasTable.groupby(['','Method']).agg(
	#how many attacks for each host
	host_count=('host', 'count'),
	#how many unique urls exist
	unique_URLS=('URL','nunique'),
	#is there an entry in the database where there is no Accept?
	Accept_exists=('Accept','all')
	#can add more here if we would like
).reset_index()
	
#debug print
print(summary_record)

#we did it... stop the connection
client.close()