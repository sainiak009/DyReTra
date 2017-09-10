from datetime import datetime
from flask_socketio import SocketIO, emit, send, join_room, leave_room
from config import app

socketio = SocketIO(app)


@socketio.on('connect', namespace="/tl")
def connectTrafficLight():
	data = {
		"cluster_id": int(datetime.timestamp(datetime.now())/10)  # TODO: Temporary
	}
	emit('get-cluster-response', {'data': data})


@socketio.on('disconnect', namespace="/tl")
def disconnectTrafficLight():
	print("Client disconnected")


@socketio.on('join-tl-cluster', namespace='/tl')
def joinTrafficCluster(data):
	tl_id = data['tl_id']
	cluster_id = data['cluster_id']  # TODO: Change Logic
	join_room(cluster_id)
	emit('cluster-response', {"data": tl_id + " Joined Cluster " + cluster_id}, room=cluster_id)
	


@socketio.on('leave-tl-cluster', namespace='/tl')
def leaveTrafficCluster(data):
	tl_id = data['tl_id']
	cluster_id = data['cluster_id']
	leave_room(cluster_id)
	emit('cluster-response', {"data": tlid + " has left the room"}, room=cluster_id)


@socketio.on('change-state', namespace='/tl')
def sendState(data):
	global_tl_id = data['global_tl_id']
	local_tl_id = data['local_tl_id']
	cluster_id = data['cluster_id']
	emit('change-state', {'data': data['message']}, room=room)


def emit_state(tl_id, cluster_id, run_time):
	print("hello")
	socketio.emit('cluster-response', {"data": tl_id + " : " + str(run_time)}, room=cluster_id)


def run():
	socketio.run(app)