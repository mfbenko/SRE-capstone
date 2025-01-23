#necessary import to get pull information out of the database
from pymongo import MongoClient
import pandas
import mysql.connector
import time

class MongoSummaryService:

	def __init__(self):
		#connecting to the mongodb
		self.client = MongoClient('mongodb://localhost:27017/')
		self.db = self.client['kafka_web_attack_data']
		self.collection = self.db['consumer_records']
		
	def __del__(self):
		self.client.close()

	def create_summary(self):
		#returns all messages in the database and creates pandas data frame
		results = self.collection.find()
		pandasTable = pandas.DataFrame(results)

		#prepare data for insertion into mySQL by creating summary records.
		summary_record = pandasTable.groupby(['','Method']).agg(
			host_count=('host', 'count'),
			unique_URLS=('URL','nunique'),
			Accept_exists=('Accept','all')
			#can add more here if we would like
		).reset_index()
		
		return summary_record
		
class SQLConnectorService:
	
	def __init__(self):		
		#create the sql connection
		self.MySQL = mysql.connector.connect(
		host='localhost',
		user='root',
		password='root'
		)

		#create a cursor write the queries
		self.cursor = self.MySQL.cursor()
		
	def __del__(self):
		self.cursor.close()
		self.MySQL.close()
		
	def create_sql_table(self):
		#create a database and table if it does not exist
		self.cursor.execute("""CREATE DATABASE IF NOT EXISTS capstone_db""")
		self.cursor.execute("""USE capstone_db""")

		self.cursor.execute("""
		CREATE TABLE IF NOT EXISTS summary(
			id INT AUTO_INCREMENT PRIMARY KEY,
			host_count INT,
			unique_URLS INT,
			Accept_exists TINYINT(1) NOT NULL DEFAULT 0
		)
		""")

	def insert_into_sql(self,summary_record):
		#insert the summary record into MySQL
		for _, row in summary_record.iterrows():
			query = """
			INSERT INTO summary (host_count, unique_URLS, Accept_exists)
			VALUES (%s, %s, %s)
			"""
			entry = (row['host_count'], row['unique_URLS'], int(row['Accept_exists']))
			self.cursor.execute(query, entry)


		#Make the commit and exit MySQL
		self.MySQL.commit()

# def main():
# 	extractor = MongoSummaryService()
# 	connector = SQLConnectorService()
# 	connector.create_sql_table()
	
# 	while True:
# 		new_summary = extractor.create_summary()
# 		connector.insert_into_sql(new_summary)
# 		print(new_summary)
# 		time.sleep(5)

	
# if __name__ == '__main__':
# 	main()