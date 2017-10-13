from .connection import Db


class TrafficSignalData(Db):
    """
       Traffic Signal Model, holds signal data for every cluster
    """

    def __init__(self, cluster_id=None):
        Db.__init__(self)
        self.coll_name = "traffic_signal_data"
        self._exists = False
        self._schema = {
            "cluster_id": None,  # String,
            "traffic_signals": [],  # Traffic signal data
            "timestamp": None  # Timestamp
        }
        if self.coll_name not in self.db.collection_names():
            self.db.create_collection(self.coll_name)
        if cluster_id:
            data = self.db[self.coll_name].find_one({"$query": {"cluster_id": str(cluster_id)}, "$orderby": {"timestamp": -1}})
            if data:
                del data['_id']
                self._schema = data

    def exists(self):
        return self._exists

    def get(self):
        return self._schema

    def create(self, data):
        self.db[self.coll_name].insert_one(data)
        return data['cluster_id']
