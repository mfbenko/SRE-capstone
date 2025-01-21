#using unitest to test consumer.py functionality
import unittest
import csv
import json
from producer import KafkaProducerService
from unittest.mock import patch, MagicMock

class TestKafkaConsuner(unittest.TestCase):
	def test_consume_messages(self):
		#do something
	def test_insert_into_mongodb(self):
		#do something
	def test_run(self):
		#do something
if __name__ == '__main__':
	unittest.main()