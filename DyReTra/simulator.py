import time
from datetime import datetime, timedelta
from random import randint

from models.trafficCluster import TrafficCluster
from sockets import emit_state
from models.allJobs import AllJobs
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import JobExecutionEvent

scheduler = BackgroundScheduler()


def _calculateTime(cluster_id, tl_id):
	"""
		Dummy function for openCV part
	"""
	run_time = (datetime.now() + timedelta(minutes=randint(1,3) + 1))
	run_time = run_time.strftime("%Y-%m-%d %H:%M:%S")
	return run_time


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
		cluster_data = cluster.get()
		if cluster_data['traffic_signals']:
			for tl_id in cluster_data['traffic_signals']:
				run_time = _calculateTime(cluster_id, tl_id)
				scheduleEvent(cluster_id, tl_id, run_time)
		else:
			raise "Cluster with no traffic signals"
	else:
		raise "Cluster doesn't exists"


def addTLtoCluster(tl_id, cluster_id):
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


def scheduleEvent(cluster_id, tl_id, run_time):
	print(run_time)
	emit_state(cluster_id, tl_id, run_time)
	new_job = scheduler.add_job(lambda: emit_state(cluster_id, tl_id, run_time), 'date', run_date=run_time)
	all_job = AllJobs()
	new_job_data = {"cluster_id": cluster_id, "tl_id": tl_id, "job_id": new_job.id}
	all_job.create(new_job_data)

def _eventListener(event):
	print(event)
	if isinstance(event, JobExecutionEvent):
		simulateCluster(job_id=event.job_id)

def run():
	scheduler.add_listener(_eventListener)
	scheduler.start()