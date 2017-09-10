from pymongo import MongoClient

client = MongoClient()
db = client.dyretra

db.traffic_cluster.insert_one({
        "cluster_id": 123456,
        "traffic_signals": ['a', 'b', 'c', 'd'],
        "coordinates": {
            "lat": 1.2,
            "long": 1.4
        }
    })

db.traffic_cluster.insert_one({
        "cluster_id": 456789,
        "traffic_signals": ['aa', 'bb', 'cc', 'dd'],
        "coordinates": {
            "lat": 1.2,
            "long": 1.4
        }
    })