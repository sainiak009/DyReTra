from connection import Db

class TrafficCluster(Db):
	"""
		Traffic Cluster model, interacting with 'traffic_cluster' document
		Args:
			cluster_id (str, optional) - Cluster Id of the Traffic Cluster

	"""
	def __init__(self, cluster_id=None):
		Db.__init__(lf)
		self.coll_name = "traffic_cluster"
		self._exists = False
		self._schema = {
			"cluster_id": None,  # string
			"traffic_signals": []  # List having TL ids
			"coordinates": {
				"lat": None,
				"long": None
			}
		}
		if self.coll_name not in self.db.collection_name():
			self.create_collection(self.coll_name, validator= {
					"validator": {
						{"cluster_id": {"$type": "string"}},
						{"traffic_signals": {"$type": "array"}}
					},
					"validation_action": "erro"
				})
		if cluster_id:
			cursor = self.db[self.coll_name].find({"cluster_id": cluster_id})
			if cursor.count() == 1:
				self._exists = True
				self._schema = cursor[0]


	def exists(self):
		return self._exists

	def get(self):
		return self._schema


	def update(self, data=None):
		if data is None:
			data = self._schema
		self.db[self.coll_name].update_one({
			"cluster_id": data['cluster_id']
			},
			{
				"$set": {
					"traffic_signals": data['traffic_signals'],
					"coordinates": data['coordinates']
				}
			})
		return data['cluster_id']

	
	def create(self, data):
		self.db[self.coll_name].insert_one(data)
		return data['cluster_id']


	def createMany(self, data):
		self.db[self.coll_name].insert_many(data)
		return True  # TODO: Change this to return cluster_ids
