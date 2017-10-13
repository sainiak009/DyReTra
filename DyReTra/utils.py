from math import radians, sin, cos, asin, acos, atan2, sqrt
from models.trafficCluster import TrafficCluster

def getReferenceLatLon():
	"""
		Returns Tuple (latitude, longitde)
	"""
	return (12.984250, 77.587972)


def getRoadSlope(lat1, lon1, lat2, lon2):
	"""
		Returns slope of the road with the line joining cluster and reference lat long'
		Args:
			lat 	- (float) Latitude
			lon 	- (float) Longitude
		Returns
			Slope 	- (float)
	"""
	# ref = getReferenceLatLon():
	dlon = (lon1 - lon2)
	y = sin(dlon) * cos(lat2)
	x = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dlon)

	bearing = atan2(y, x)
	return bearing

def getEVClusters(lat, lon, radius=5):
	all_clusters = TrafficCluster().getAllNearby(lat, lon, radius)
	return all_clusters
