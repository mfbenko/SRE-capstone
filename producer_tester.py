#using unitest to test producer.py functionality
import unittest
from producer import KafkaProducerService
from unittest.mock import patch, MagicMock

class TestKafkaProducer(unittest.TestCase):
    
	@patch.object(KafkaProducerService, 'send_message')
	@patch.object(KafkaProducerService, 'create_producer')
	#create a mock producer using producer.py's create_procer method
	def test_send_message(self, mock_create_producer, mock_send_message):
		producer = KafkaProducerService()
		mock_producer = MagicMock()
		mock_create_producer.return_value = mock_producer
		producer.create_producer('test_database.csv')
		producer.send_message()
		mock_send_message.assert_called_once()
		mock_create_producer.assert_called_once()

	@patch.object(KafkaProducerService, 'create_producer')
	def test_producer_creation(self, mock_create_producer):
		producer = KafkaProducerService()
		producer_create_test = mock_create_producer.return_value
		producer.create_producer()
		mock_create_producer.assert_called_once()

if __name__ == '__main__':
	unittest.main()
