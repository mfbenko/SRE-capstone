#necessary import to get pull information out of the database
from pymongo import MongoClient
import pandas
import mysql.connector
import time
import os

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
		self.cursor.execute("""CREATE DATABASE IF NOT EXISTS capstone_db;""")
		self.cursor.execute("""USE capstone_db;""")

		self.cursor.execute("""
		CREATE TABLE IF NOT EXISTS summary(
			id INT AUTO_INCREMENT PRIMARY KEY,
			host_count INT,
			unique_URLS INT,
			Accept_exists TINYINT(1) NOT NULL DEFAULT 0
		)
		""")

	def insert_into_sql(self,summary_record):
		#we want to overwrite not add new rows
		self.cursor.execute("""DELETE FROM SUMMARY;""")
	
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
		
	def sql_extract(self):
		#This script is strictly for the capstone_db and summary table
		self.cursor.execute("""USE capstone_db;""")
		
		#print the hard coded host count to the screen
		print("Total hosts encountered:")
		self.cursor.execute("""SELECT host_count FROM summary;""")
		results = self.cursor.fetchall()
		type = "get: "
		for row in results:
			print(f"{type}{row[0]}")
			type = "post: "
		print("\n")

		#print the hard coded url count to the screen
		print("Total unique URLS encountered:")
		self.cursor.execute("""SELECT unique_URLS FROM summary;""")
		results = self.cursor.fetchall()
		type = "get: "
		for row in results:
			print(f"{type}{row[0]}")
			type = "post: "
		print("\n")
			
		#print the hard coded accept boolean to the screen
		print("Accept exists:")
		self.cursor.execute("""SELECT Accept_exists FROM summary;""")
		results = self.cursor.fetchall()
		type = "get: "
		for row in results:
			print(f"{type}{row[0]}")
			type = "post: "
			
		print("\n")

<<<<<<< HEAD
# def main():
# 	extractor = MongoSummaryService()
# 	connector = SQLConnectorService()
# 	connector.create_sql_table()
	
# 	while True:
# 		new_summary = extractor.create_summary()
# 		connector.insert_into_sql(new_summary)
# 		print(new_summary)
# 		time.sleep(5)
=======
def main():
	extractor = MongoSummaryService()
	connector = SQLConnectorService()
	connector.create_sql_table()

	while True:
		new_summary = extractor.create_summary()
		connector.insert_into_sql(new_summary)
		connector.sql_extract()
		time.sleep(5)
		os.system('cls')
>>>>>>> 738f916f9e904d3adcab22881460eaa362ab26b3

	
# if __name__ == '__main__':
# 	main()