import operator
from random import randint
from datetime import datetime

from models.trafficCluster import TrafficCluster
from sockets import emit_state
from utils import getRoadSlope
from models.allJobs import AllJobs
from models.trafficSignalData import TrafficSignalData
from api import getSnap
from image import getTrafficData


def _simulateTrafficDensity(cluster_id):
    """
        Get Traffic Density for a cluster
        Args
            cluster_id - Cluster Id of existing cluster
        Returns
            {
                "a": 0.5,
                "b": 0.6
            }
    """
    if not cluster_id:
        raise "Cluster Id is required"
    cluster = TrafficCluster(cluster_id=cluster_id)
    tl_density = {}
    if cluster.exists():
        cluster_data = cluster.get()
        image_path = getSnap(cluster_data['coordinates']['lat'], cluster_data['coordinates']['lon'])
        print(image_path)
        traffic_data = getTrafficData(image_path)
        traffic_lights_data = cluster.getTrafficLights()
        print(traffic_lights_data)

        #     if traffic_lights_data:
        #         for tl in traffic_lights_data:
        #             tl_density[tl["tl_id"]] = randint(2, 5) / 100
        #     else:
        #         raise "Cluster with no traffic signals"
        # else:
        #     raise "Cluster doesn't exists"
    return True #tl_density


def _calculateTime(cluster_id):
    """
        Generates traffic light actions according to traffic density
        Args
            cluster_density - {"tl_id1": density1, "tl_id2": density}, (0 < density < 1)
        Returns
            {
                "no_of_cycles": N,
                "traffic_signals": [ {}, {}, {} ] (N dictionaries)
            }
    """
    cluster_density = _simulateTrafficDensity(cluster_id)
    sorted_cluster_density = sorted(cluster_density.items(), key=operator.itemgetter(1), reverse=True)
    traffic_signals = []
    total_time = 0
    for i in sorted_cluster_density:
        temp = {}
        green_time = int(i[1] * 100)
        temp['tl_id'] = i[0]
        temp['timer'] = green_time
        traffic_signals.append(temp)
        total_time += green_time
    return traffic_signals, total_time


def simulateCluster(cluster_id=None, job_id=None):
    """
        This will start the cluster simulation
        Args
            cluster_id - Cluster Id of existing cluster
    """
    if cluster_id is None and job_id is None:
        raise "Atleast one of cluster id or job id is required"

    if job_id:
        job_data = AllJobs(job_id=job_id)
        cluster_id = job_data['cluster_id']

    cluster = TrafficCluster(cluster_id=cluster_id)
    if cluster.exists():
        traffic_lights_data = cluster.getTrafficLights()
        if traffic_lights_data:
            tl_signal = _calculateTime(cluster_id)
            scheduleEvent(cluster_id, tl_signal[0], tl_signal[1])
        else:
            raise "Cluster with no traffic signals"
    else:
        raise "Cluster doesn't exists"


def addTLtoCluster(tl_id, cluster_id):
    """
        Adds Traffic Light to corresponding Cluster
    """
    cluster = TrafficCluster(cluster_id=cluster_id)
    if cluster.exists():
        cluster_data = cluster.get()
        cluster_data['traffic_signals'].append(tl_id)
        cluster.update(cluster_data)
        return True
    else:
        raise "Cluster doen't exists"
        return False


def createCluster(cluster_data):
    """
        Inserts cluster data in db
        Args
            cluster_data (dict) - Structure same as TrafficCluster Schema
    """
    cluster = TrafficCluster(cluster_data['cluster_id'])
    if cluster.exists():
        raise "Cluster Id already exists"
        return False
    else:
        cluster.create(cluster_data)
    return True


def scheduleEvent(cluster_id, tl_signal, total_time):
    time_now = datetime.now()
    ts = TrafficSignalData()
    ts.create({"cluster_id": cluster_id, "traffic_signals": tl_signal, "timestamp": int(time_now.timestamp())})
    emit_state(cluster_id, tl_signal, total_time, int(time_now.timestamp()))


def changeClusterStatusforEV(cluster_id, lat, lon):
    cluster = TrafficCluster(cluster_id)
    cluster_signal_data = TrafficSignalData(cluster_id)
    if cluster.exists():
        traffic_lights_data = cluster.getTrafficLights()
        if traffic_lights_data:
            for tl in traffic_lights_data:
                if tl['slope'] == getRoadSlope(cluster['coordinates']['lat'], cluster['coordinates']['lon'], lat, lon):
                    break
    else:
        pass


print(_simulateTrafficDensity(123456))
