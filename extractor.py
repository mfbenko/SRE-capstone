#necessary import to get pull information out of the database
import asyncio
from pymongo import MongoClient
import pandas
import mysql.connector
import time
import os

class MongoSummaryService:

	def __init__(self, logger=None):
		#connecting to the mongodb
		self.client = MongoClient('mongodb://localhost:27017/')
		self.db = self.client['kafka_web_attack_data']
		self.collection = self.db['consumer_records']
		self.logger = logger
		
	def __del__(self):
		self.client.close()

	def create_summary(self):
		print("EXTRACTOR: Creating Summary Record")
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
	
	async def run(self):
		self.logger.info("EXTRACTOR: Runing now...")
		while True:
			try:
				self.logger.info("EXTRACTOR: Inside extraction loop")
				new_summary = self.create_summary()
				self.logger.info(f"\n\033[38;5;202mInserted new summary:\033[0m\n{new_summary}") if self.logger is not None else None
			except Exception as e:
				self.logger.error(f"Error during extraction or insertion: {e}") if self.logger is not None else None
			await asyncio.sleep(5)
		
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