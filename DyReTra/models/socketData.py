from models.connection import Db


class SocketData(Db):
    """
       Traffic Signal Model, holds signal data for every cluster
    """

    def __init__(self, sid=None):
        Db.__init__(self)
        self.coll_name = "traffic_signal_data"
        self._exists = False
        self._schema = {
            "cluster_id": None,  # String,
            "tl_id": [],  # Traffic signal data
            "sid": None,
            "status": None,  # 0 or 1
            "timestamp": None  # timestamp
        }
        if self.coll_name not in self.db.collection_names():
            self.db.create_collection(self.coll_name)
        if sid:
            data = self.db[self.coll_name].find_one({"$query": {"sid": str(sid)}, "$orderby": {"timestamp": -1}})
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
        return data['sid']

    def update_status(self, status):
        self._schema['status'] = status
        self.db[self.coll_name].update_one({"sid": self._schema['sid']}, {"$set": {"status": status}})

    def get_active_tlid(self, cluster_id):
        data = self.db[self.coll_name].find_one({"cluster_id": cluster_id, "status": 1})
        if data:
            return data['tl_id']
        else:
            return None
