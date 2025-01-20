#using unitest to test producer.py functionality
import unittest
from producer import KafkaProducerService
from unittest.mock import patch

class TestKafkaProducer(unittest.TestCase):
    
	#create a mock producer using producer.py's create_procer method
	def test_send_message(self):
		producer = KafkaProducerService()
		producer.create_producer('test_database.csv')
		producer.send_message()
		mock_produce.assert_called_once()
		mock_flush.assert_called_once()

	'''@patch('producer.KafkaProducerService.create_producer')
	def test_producer_creation(self, mock_create_producer):
		producer = KafkaProducerService()
		# Test that create_producer is being called and behaves correctly
		producer_create_test = mock_create_producer.return_value

		# Call your producer creation logic
		producer.create_producer()

		# Ensure that the producer was created with correct configuration
		mock_create_producer.assert_called_once()
		#self.assertEqual(producer, mock_create_producer.return_value)'''

if __name__ == '__main__':
	unittest.main()
