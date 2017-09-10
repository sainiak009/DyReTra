from pymongo import MongoClient

class Db:
	def __init__(self):
		self.client = MongoClient()
		self.db = client.test_database