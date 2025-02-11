#using unitest to test consumer.py functionality
import unittest
import sys
import os
from unittest.mock import MagicMock
import asyncio
from pymongo.collection import Collection

#Add the 'src' folder to the sys.path inorder to gain acces to kfkaConsumerService
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from consumer import KafkaConsumerService

class TestKafkaConsuner(unittest.TestCase):
	#mock the consumer instance so that each test can be isolated
	def setUp(self):
		self.mock_consumer = MagicMock()
		
		self.consumer_instance = KafkaConsumerService(
			topic="my_topic_test",
			bootstrap_servers=["localhost:9092"],
			mongo_uri="mongodb://localhost:27017/",
			database_name="kafka_web_attack_test",
			collection_name="consumer_records_test"
		)
		self.consumer_instance.consumer = self.mock_consumer
		self.mock_collection = MagicMock()
		self.consumer_instance.collection_name = self.mock_collection
		  
	#using the mock consumer we will test to see if the messages consumed match the expected output
	def test_consume_messages(self):
		messages = [
			MagicMock(value={'': 'Anomalous', 'Method': '', 'User-Agent': '', 'Pragma': '', 'Cache-Control': '', 'Accept': '', 'Accept-encoding': '', 'Accept-charset': '', 'language': '', 'host': '', 'cookie': '', 'content-type': '', 'connection': '', 'lenght': '', 'content': '', 'classification': '', 'URL': ''}),
			MagicMock(value={'': 'Normal', 'Method': 'GET', 'User-Agent': 'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.8 (like Gecko)', 'Pragma': 'no-cache', 'Cache-Control': 'no-cache', 'Accept': 'text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5', 'Accept-encoding': 'x-gzip, x-deflate, gzip, deflate', 'Accept-charset': 'utf-8, utf-8;q=0.5, *;q=0.5', 'language': 'en', 'host': 'localhost:8080', 'cookie': 'JSESSIONID=81761ACA043B0E6014CA42A4BCD06AB5', 'content-type': '', 'connection': 'close', 'lenght': '', 'content': '', 'classification': '0', 'URL': 'http://localhost:8080/tienda1/publico/anadir.jsp?id=3&nombre=Vino+Rioja&precio=100&cantidad=55&B1=A%F1adir+al+carrito HTTP/1.1'}),
			MagicMock(value={'': 'Anomalous', 'Method': '1', 'User-Agent': '2', 'Pragma': '3', 'Cache-Control': '4', 'Accept': '5', 'Accept-encoding': '6', 'Accept-charset': '7', 'language': '8', 'host': '9', 'cookie': '10', 'content-type': '11', 'connection': '12', 'lenght': '13', 'content': '14', 'classification': '15', 'URL': '16'}),
			MagicMock(value={'': 'Normal', 'Method': '', 'User-Agent': 'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.8 (like Gecko)', 'Pragma': 'no-cache', 'Cache-Control': 'no-cache', 'Accept': 'text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5', 'Accept-encoding': 'x-gzip, x-deflate, gzip, deflate', 'Accept-charset': 'utf-8, utf-8;q=0.5, *;q=0.5', 'language': 'en', 'host': 'localhost:8080', 'cookie': '', 'content-type': '', 'connection': 'close', 'lenght': '', 'content': '', 'classification': '0', 'URL': ''})
		]


		self.mock_consumer.__iter__.return_value = iter(messages)
		received_data = list(self.consumer_instance.consume_messages())

		expected_data = [
			{'': 'Anomalous', 'Method': '', 'User-Agent': '', 'Pragma': '', 'Cache-Control': '', 'Accept': '', 'Accept-encoding': '', 'Accept-charset': '', 'language': '', 'host': '', 'cookie': '', 'content-type': '', 'connection': '', 'lenght': '', 'content': '', 'classification': '', 'URL': ''},
			{'': 'Normal', 'Method': 'GET', 'User-Agent': 'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.8 (like Gecko)', 'Pragma': 'no-cache', 'Cache-Control': 'no-cache', 'Accept': 'text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5', 'Accept-encoding': 'x-gzip, x-deflate, gzip, deflate', 'Accept-charset': 'utf-8, utf-8;q=0.5, *;q=0.5', 'language': 'en', 'host': 'localhost:8080', 'cookie': 'JSESSIONID=81761ACA043B0E6014CA42A4BCD06AB5', 'content-type': '', 'connection': 'close', 'lenght': '', 'content': '', 'classification': '0', 'URL': 'http://localhost:8080/tienda1/publico/anadir.jsp?id=3&nombre=Vino+Rioja&precio=100&cantidad=55&B1=A%F1adir+al+carrito HTTP/1.1'},
			{'': 'Anomalous', 'Method': '1', 'User-Agent': '2', 'Pragma': '3', 'Cache-Control': '4', 'Accept': '5', 'Accept-encoding': '6', 'Accept-charset': '7', 'language': '8', 'host': '9', 'cookie': '10', 'content-type': '11', 'connection': '12', 'lenght': '13', 'content': '14', 'classification': '15', 'URL': '16'},
			{'': 'Normal', 'Method': '', 'User-Agent': 'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.8 (like Gecko)', 'Pragma': 'no-cache', 'Cache-Control': 'no-cache', 'Accept': 'text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5', 'Accept-encoding': 'x-gzip, x-deflate, gzip, deflate', 'Accept-charset': 'utf-8, utf-8;q=0.5, *;q=0.5', 'language': 'en', 'host': 'localhost:8080', 'cookie': '', 'content-type': '', 'connection': 'close', 'lenght': '', 'content': '', 'classification': '0', 'URL': ''}
		]

		self.assertEqual(received_data, expected_data)
	
	#make sure that when a message is inserted into mongo that it doesn't throw an exception
	def test_insert_into_mongodb(self):
		try:
			message ={'': 'Anomalous', 'Method': '', 'User-Agent': '', 'Pragma': '', 'Cache-Control': '', 'Accept': '', 'Accept-encoding': '', 'Accept-charset': '', 'language': '', 'host': '', 'cookie': '', 'content-type': '', 'connection': '', 'lenght': '', 'content': '', 'classification': '', 'URL': ''}
			self.consumer_instance.insert_into_mongodb(message)
		except Exception as e:
			self.fail(f"An exception was raised: {e}")
			
	#make sure that insertion of everything into mongo and no exception is thrown
	def test_run(self):
		try:
			messages = [
				MagicMock(value={'': 'Anomalous', 'Method': '', 'User-Agent': '', 'Pragma': '', 'Cache-Control': '', 'Accept': '', 'Accept-encoding': '', 'Accept-charset': '', 'language': '', 'host': '', 'cookie': '', 'content-type': '', 'connection': '', 'lenght': '', 'content': '', 'classification': '', 'URL': ''}),
				MagicMock(value={'': 'Normal', 'Method': 'GET', 'User-Agent': 'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.8 (like Gecko)', 'Pragma': 'no-cache', 'Cache-Control': 'no-cache', 'Accept': 'text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5', 'Accept-encoding': 'x-gzip, x-deflate, gzip, deflate', 'Accept-charset': 'utf-8, utf-8;q=0.5, *;q=0.5', 'language': 'en', 'host': 'localhost:8080', 'cookie': 'JSESSIONID=81761ACA043B0E6014CA42A4BCD06AB5', 'content-type': '', 'connection': 'close', 'lenght': '', 'content': '', 'classification': '0', 'URL': 'http://localhost:8080/tienda1/publico/anadir.jsp?id=3&nombre=Vino+Rioja&precio=100&cantidad=55&B1=A%F1adir+al+carrito HTTP/1.1'}),
				MagicMock(value={'': 'Anomalous', 'Method': '1', 'User-Agent': '2', 'Pragma': '3', 'Cache-Control': '4', 'Accept': '5', 'Accept-encoding': '6', 'Accept-charset': '7', 'language': '8', 'host': '9', 'cookie': '10', 'content-type': '11', 'connection': '12', 'lenght': '13', 'content': '14', 'classification': '15', 'URL': '16'}),
				MagicMock(value={'': 'Normal', 'Method': '', 'User-Agent': 'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.8 (like Gecko)', 'Pragma': 'no-cache', 'Cache-Control': 'no-cache', 'Accept': 'text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5', 'Accept-encoding': 'x-gzip, x-deflate, gzip, deflate', 'Accept-charset': 'utf-8, utf-8;q=0.5, *;q=0.5', 'language': 'en', 'host': 'localhost:8080', 'cookie': '', 'content-type': '', 'connection': 'close', 'lenght': '', 'content': '', 'classification': '0', 'URL': ''})
			]
			
			self.consumer_instance.insert_into_mongodb = MagicMock()
			self.mock_consumer.__iter__.return_value = iter(messages)
			self.consumer_instance.consume_messages()
			asyncio.run(self.consumer_instance.run())
			self.consumer_instance.insert_into_mongodb.assert_called()
			
		except Exception as e:
			self.fail(f"An exception was raised: {e}")
	
	#after every test close the connection to mongo so that it isn't left open
	def tearDown(self):
		self.consumer_instance.mongo_client.close()
		
if __name__ == '__main__':
	unittest.main()