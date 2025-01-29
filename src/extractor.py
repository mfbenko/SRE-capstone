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
		# self.collection.delete_many({})
		self.logger = logger
		
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
			#can add more here if we would like
		).reset_index()
		return summary_record
	
	async def run(self, connector=None):
		while True:
			try:
				new_summary = self.create_summary()
				self.logger.info(f"\n\033[38;5;202mInserted new summary:\033[0m\n{new_summary}") if self.logger is not None else None
				connector.insert_into_sql(new_summary) if connector is not None else None
				connector.sql_extract()
			except Exception as e:
				self.logger.error(f"Error during extraction or insertion: {e}") if self.logger is not None else None
			finally:
				await asyncio.sleep(5)
			
		
class SQLConnectorService:
	
	def __init__(self,logger=None):		
		#create the sql connection
		self.MySQL = mysql.connector.connect(
		host='localhost',
		user='root',
		password='root'
		)
		#create a cursor write the queries
		self.cursor = self.MySQL.cursor()
		self.logger = logger
		
	def __del__(self):
		self.cursor.close()
		self.MySQL.close()
		
	def create_sql_table(self):
		try:
			self.cursor.execute("""USE capstone_db;""")
			self.cursor.execute("DROP TABLE IF EXISTS summary;")
			self.MySQL.commit()
			self.logger.info("\033[91m\nTable 'summary' dropped successfully.\033[0m") if self.logger is not None else None
		except mysql.connector.Error as err:
			self.logger.error(f"Error dropping table: {err}") if self.logger is not None else None
	
		#create a database and table if it does not exist
		self.cursor.execute("""CREATE DATABASE IF NOT EXISTS capstone_db;""")
		self.cursor.execute("""USE capstone_db;""")

		self.cursor.execute("""
		CREATE TABLE IF NOT EXISTS summary(
			id INT AUTO_INCREMENT PRIMARY KEY,
			type VARCHAR(225),
			Method VARCHAR(255),
			host_count INT,
			unique_URLS INT
		)
		""")

	def insert_into_sql(self,summary_record):
		#we want to overwrite not add new rows
		self.cursor.execute("""DELETE FROM SUMMARY;""")
		#insert the summary record into MySQL
		for _, row in summary_record.iterrows():
			query = """
			INSERT INTO summary (type, Method, host_count, unique_urls)
			VALUES (%s, %s, %s, %s)
			"""
			entry = (row[''], row['Method'], row['host_count'], row['unique_URLS'])
			self.cursor.execute(query, entry)
		#Make the commit and exit MySQL
		self.MySQL.commit()
		self.logger.info("\033[93m\nInserting and commiting to MySQL.\033[0m") if self.logger is not None else None
		
	def sql_extract(self):
		#This script is strictly for the capstone_db and summary table
		self.cursor.execute("""USE capstone_db;""")
		#print the hard coded host count to the screen
		self.logger.info("\033[93mInformation Inseterd into SQL:\033[0m") if self.logger is not None else None
		self.cursor.execute("""SELECT type, Method, host_count, unique_URLS FROM summary;""")
		results = self.cursor.fetchall()
		for _, data in enumerate(results):
			self.logger.info(f"type: {data[0]}, method: {data[1]}, host_count: {data[2]}, unique_URLS: {data[3]}") if self.logger is not None else None
			
		self.logger.info("\n") if self.logger is not None else None