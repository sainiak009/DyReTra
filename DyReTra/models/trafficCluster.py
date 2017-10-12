from .connection import Db


class TrafficCluster(Db):
    """
        Traffic Cluster model, interacting with 'traffic_cluster' document
        Args:
            cluster_id (str, optional) - Cluster Id of the Traffic Cluster

    """

    def __init__(self, cluster_id=None):
        Db.__init__(self)
        self.coll_name = "traffic_cluster"
        self._exists = False
        self._schema = {
            "cluster_id": None,  # string
            "roads": [],  # List having TL ids
            "coordinates": {
                "lat": None,
                "long": None
            }
        }
        if self.coll_name not in self.db.collection_names():
            self.db.create_collection(self.coll_name)
        if cluster_id:
            cursor = self.db[self.coll_name].find({"cluster_id": int(cluster_id)})
            for c in cursor:
                self._schema = c
            if cursor.count() == 1:
                self._exists = True

    def _validateData(self, data):
        if data["approach_fl"] == 0 and data["traffic_signal"] != {}:
            return False
        return True

    def getRoadDictStr(self):
        road_dict = {
            "road_id": None,
            "approach_fl": None,
            "slope": None,
            "cv_coord": [],
            "traffic_signal": {}
        }
        return road_dict

    def getTrafficLights(self):
        all_signals = []
        for road in self._schema['roads']:
            if road['approach_fl'] == 1:
                all_signals.append({
                    "tl_id": road['traffic_signal']['id']
                })
        return all_signals

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
                    "roads": data['roads'],
                    "coordinates": data['coordinates']
                }
            })
        return data['cluster_id']

    def create(self, data):
        # if self._validateData(data):
        if True: # TODO
            self.db[self.coll_name].insert_one(data)
            return data['cluster_id']
        return False

    def createMany(self, data):
        self.db[self.coll_name].insert_many(data)
        return True  # TODO: Change this to return cluster_ids
