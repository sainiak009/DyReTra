from sockets import emit_change
from simulator import simulateCluster
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import JobExecutionEvent

scheduler = BackgroundScheduler()

def scheduleEvent(cluster_id, tl_id, run_time):
	scheduler.add_job(emit_change(cluster_id, tl_id, run_time), 'date', run_date=run_time)
	# insert above job info in db (will be used to set next event)

def _eventListener(event):
	if isinstance(event, JobExecutionEvent):
		nextRun()