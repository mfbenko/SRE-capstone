#necessary import to get pull information out of the database
from pymongo import MongoClient
import pandas
import mysql.connector

#connecting to the mongodb
client = MongoClient('mongodb://localhost:27017/')
db = client['kafka_web_attack_data']
collection = db['consumer_records']

#returns all messages in the database and creates pandas data frame
results = collection.find()
pandasTable = pandas.DataFrame(results)
	
#prepare data for insertion into mySQL by creating summary records.
summary_record = pandasTable.groupby(['','Method']).agg(
	host_count=('host', 'count'),
	unique_URLS=('URL','nunique'),
	Accept_exists=('Accept','all')
	#can add more here if we would like
).reset_index()
	
#debug print
print(summary_record)

#create the sql connection
MySQL = mysql.connector.connect(
	host='localhost',
	user='root',
	password='root'
)

#create a cursor write the queries
cursor = MySQL.cursor()

#create a database and table if it does not exist
cursor.execute("""CREATE DATABASE IF NOT EXISTS capstone_db""")
cursor.execute("""USE capstone_db""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS summary(
	id INT AUTO_INCREMENT PRIMARY KEY,
	host_count INT,
	unique_URLS INT,
	Accept_exists TINYINT(1) NOT NULL DEFAULT 0
)
""")

#insert the summary record into MySQL
for _, row in summary_record.iterrows():
    query = """
    INSERT INTO summary (host_count, unique_URLS, Accept_exists)
    VALUES (%s, %s, %s)
    """
    entry = (row['host_count'], row['unique_URLS'], int(row['Accept_exists']))
    cursor.execute(query, entry)


#Make the commit and exit MySQL
MySQL.commit()
cursor.close()
MySQL.close()

#we did it... stop the connection
client.close()