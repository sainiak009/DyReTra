from .connection import Db
from math import radians, sin, cos, asin, acos, atan2, sqrt

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
                "lon": None
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

    def getAllTrafficLights(self):
        all_signals = []
        for road in self._schema['roads']:
            all_signals.append({
                "tl_id": road['traffic_signal']['id'],
                "approach_fl": road['approach_fl']
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


    def iswithinRange(self, lat1, lon1, lat2, lon2, radius):
        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 6371 # Radius of earth in kilometers. Use 3956 for miles
        if c*r <= radius:
            return True
        else:
            return False


    def getAllNearby(self, lat, lon, radius=5):
        all_nearby = []
        for i in self.db[self.coll_name].find():
            if self.iswithinRange(lat, lon, i["coordinates"]["lat"], i["coordinates"]["lon"], radius):
                all_nearby.append({
                    "cluster_id": i['cluster_id'],
                    "coordinates": {
                        "lat": i["coordinates"]["lat"],
                        "lon": i["coordinates"]["lon"]
                    }
                })
        return all_nearby
