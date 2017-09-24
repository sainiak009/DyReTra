from DyReTra.models.trafficCluster import TrafficCluster

if __name__ == "__main__":
    t = TrafficCluster()
    t.create({'coordinates': {'long': 1.4, 'lat': 1.2}, 'cluster_id': 123456, 'traffic_signals': ['a', 'b', 'c', 'd']})
    t.create({'coordinates': {'long': 1.5, 'lat': 1.3}, 'cluster_id': 456789, 'traffic_signals': ['aa', 'bb', 'cc', 'dd']})
    t.create({'coordinates': {'long': 1.6, 'lat': 1.4}, 'cluster_id': 789456, 'traffic_signals': ['aaa', 'bbbb', 'ccc', 'dddd']})
    t.create({'coordinates': {'long': 1.7, 'lat': 1.5}, 'cluster_id': 456123, 'traffic_signals': ['ab', 'ba', 'cd', 'dc']})
    t.create({'coordinates': {'long': 1.8, 'lat': 1.6}, 'cluster_id': 789123, 'traffic_signals': ['ac', 'bd', 'ca', 'db']})
