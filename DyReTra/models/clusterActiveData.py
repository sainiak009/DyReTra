from models.connection import Db


class ClusterActiveData(Db):
    """
       Traffic Signal Model, holds signal data for every cluster
    """

    def __init__(self, cluster_id=None):
        Db.__init__(self)
        self.coll_name = "cluster_active_data"
        self._exists = False
        self._schema = {
            "cluster_id": None,  # String,
            "alive_connection": None,  # Traffic signal data
            "simulator_tl_id": None,
            "timestamp": None  # Timestamp
        }
        if self.coll_name not in self.db.collection_names():
            self.db.create_collection(self.coll_name)
        if cluster_id:
            data = self.db[self.coll_name].find_one({"$query": {"cluster_id": str(cluster_id)}, "$orderby": {"timestamp": -1}})
            if data:
                del data['_id']
                self._schema = data
                self._exists = True

    def exists(self):
        return self._exists

    def get(self):
        return self._schema

    def create(self, data):
        self.db[self.coll_name].insert_one(data)
        return data['cluster_id']

    def increment(self):
        self._schema['alive_connection'] += 1
        self.db[self.coll_name].update_one({"cluster_id": self._schema['cluster_id']}, {"$set": {"alive_connection": self._schema['alive_connection']}})

    def decrement(self):
        self._schema['alive_connection'] -= 1
        self.db[self.coll_name].update_one({"cluster_id": self._schema['cluster_id']}, {"$set": {"alive_connection": self._schema['alive_connection']}})
