from models.connection import Db


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
            cursor = self.db[self.coll_name].find({"cluster_id": int(cluster_id)})
            for c in cursor:
                self._schema = c
            if cursor.count() == 1:
                self._exists = True

    def exists(self):
        return self._exists

    def get(self):
        return self._schema

    def create(self, data):
        self.db[self.coll_name].insert_one(data)
        return data['cluster_id']
