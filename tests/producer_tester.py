#using unitest to test producer.py functionality
import unittest
import sys
import os
import csv
import json
from unittest.mock import patch

#Add the 'src' folder to the sys.path inorder to gain acces to kfkaProducerService
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from producer import KafkaProducerService

class TestKafkaProducer(unittest.TestCase):
    #use the test database csv file to make sure that serialization works
	def test_json_serializer(self):
		mock_topic = 'test_topic'
		mock_bootstrap_servers = 'localhost:9092'
		mock_file = 'test_database.csv'
		producer = KafkaProducerService(mock_topic, mock_bootstrap_servers, mock_file)
		with open('test_database.csv', 'r') as file:
			csv_reader = csv.DictReader(file)
			rows = list(csv_reader)
		for row in rows:
			serialized_data=KafkaProducerService.json_serializer(row)
			expected_serialized_data = json.dumps(row).encode('utf-8')
			self.assertEqual(serialized_data, expected_serialized_data)
			
	#test to see if creating a producer is successful
	def test_producer_creation(self):
		mock_topic = 'test_topic'
		mock_bootstrap_servers = 'localhost:9092'
		mock_file = 'test_database.csv'
		producer = KafkaProducerService(mock_topic, mock_bootstrap_servers, mock_file)
		self.assertIsNotNone(producer.producer)

	#create a producer and test its send_message method completes calls to send() 4 times
	@patch('kafka.KafkaProducer.send')
	def test_run(self, mock_send):
		mock_topic = 'test_topic'
		mock_bootstrap_servers = 'localhost:9092'
		mock_file = 'test_database.csv'
		producer = KafkaProducerService(mock_topic, mock_bootstrap_servers, mock_file)
		producer.run()
		self.assertEqual(mock_send.call_count, 4)
		
if __name__ == '__main__':
	unittest.main()