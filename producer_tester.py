#using unitest to test producer.py functionality
import unittest
import csv
import json
from producer import KafkaProducerService
from unittest.mock import patch, MagicMock

class TestKafkaProducer(unittest.TestCase):
    #use the test database csv file to make sure that serialization works
	def test_json_serializer(self):
		producer = KafkaProducerService()
		with open('test_database.csv', 'r') as file:
			csv_reader = csv.DictReader(file)
			rows = list(csv_reader)
		for row in rows:
			serialized_data=KafkaProducerService.json_serializer(row)
			expected_serialized_data = json.dumps(row).encode('utf-8')
			self.assertEqual(serialized_data, expected_serialized_data)
			
	#test to see if creating a producer is successful
	def test_producer_creation(self):
		producer = KafkaProducerService()
		producer.create_producer('test_database.csv')
		self.assertIsNotNone(producer.producer)

	#create a producer and test its send_message method completes calls to send() 4 times
	@patch('kafka.KafkaProducer.send')
	def test_send_message(self, mock_send):
		producer = KafkaProducerService()
		producer.create_producer('test_database.csv')
		producer.send_message()
		self.assertEqual(mock_send.call_count, 4)
		
if __name__ == '__main__':
	unittest.main()