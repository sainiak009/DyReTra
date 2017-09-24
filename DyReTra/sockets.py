from datetime import datetime
from flask_socketio import SocketIO, emit, send, join_room, leave_room
from config import app

from models.trafficCluster import TrafficCluster
from models.trafficSignalData import TrafficSignalData

socketio = SocketIO(app)


@socketio.on('connect', namespace="/tl")
def connectTrafficLight():
    data = {
        "cluster_id": int(datetime.timestamp(datetime.now()) / 10)  # TODO: Temporary
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
    cluster = TrafficCluster(cluster_id)
    cluster_data = cluster.get()
    del cluster_data['_id']
    emit('join-cluster-response', {"message": tl_id + " Joined Cluster " + cluster_id, "cluster_data": cluster_data}, room=cluster_id)
    cluster_signal = TrafficSignalData(cluster_id)
    cluster_signal_data = cluster_signal.get()
    emit('simulate-cluster-response',
         {"message": "Signal Received", "data": cluster_signal_data['traffic_signals'], "timestamp": cluster_signal_data['timestamp']},
         room=cluster_id,
         namespace='/tl')


@socketio.on('leave-tl-cluster', namespace='/tl')
def leaveTrafficCluster(data):
    tl_id = data['tl_id']
    cluster_id = data['cluster_id']
    leave_room(cluster_id)
    emit('cluster-response', {"data": tl_id + " has left the room"}, room=cluster_id)


@socketio.on('change-state', namespace='/tl')
def sendState(data):
    # global_tl_id = data['global_tl_id']
    # local_tl_id = data['local_tl_id']
    cluster_id = data['cluster_id']
    emit('change-state', {'data': data['message']}, room=cluster_id)


def emit_state(cluster_id, tl_signal, total_time, timestamp):
    print("++ emit state ++")
    socketio.emit('simulate-cluster-response', {"message": "Signal Received", "data": tl_signal, "timestamp": timestamp}, room=cluster_id, namespace="/tl")


def run():
    socketio.run(app, debug=True)
