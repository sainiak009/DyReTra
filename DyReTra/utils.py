import math
from models.trafficCluster import TrafficCluster

def iswithinRange():
	pass

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
	y = math.sin(dlon) * math.cos(lat2)
	x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)

	bearing = math.atan2(y, x)
	return bearing

def getEVClusters(lat, lon):
	pass

print(getRoadSlope(12.979268, 77.602457, 12.979490, 77.601711))
print(getRoadSlope(12.979268, 77.602457, 12.978925, 77.603414))
print(getRoadSlope(12.979268, 77.602457, 12.978766, 77.602317))
print(getRoadSlope(12.979268, 77.602457, 12.979882, 77.602649))