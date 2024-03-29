from config import app
from sockets import run as start_socket
from simulator import simulateCluster, changeClusterStatusforEV
from flask import render_template, request, send_from_directory
from flask_restful import Api
from config_values import GOOGLE_KEY
from api import *

import simplejson as json

from utils import getEVClusters

api = Api(app)

# All Api routes will go here
api.add_resource(getDirectionsEV, '/getDirectionsEV')
api.add_resource(getMapSnap, '/getMapSnap')


# Static files routes
@app.route('/img/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

# All general routes will go here
@app.route('/signal')
def traffic_signal():
    return render_template('traffic_signal.html')


@app.route('/start_cluster_simulation', methods=['POST', 'GET'])
def start_cluster_simulator():
    simulateCluster(cluster_id=request.args.get('cluster_id', None))
    return request.args.get('cluster_id', 'Hola')


@app.route('/trafficSnap/<lat>/<lon>')  # To generate traffic layers
def traffic_snap(lat, lon):
    return render_template('traffic_layer.html', latitude=lat, longitude=lon)


@app.route('/EVSimulator')	 # Emergency Vehicles Simulations
def EV_simulator():
    return render_template('ev_simulation.html', GOOGLE_KEY=GOOGLE_KEY)


@app.route('/getNearbyCluster', methods=['POST', 'GET'])
def getNearbyCluster():
    ev_id = request.args.get('ev_id', None)
    lat = request.args.get('lat', None)
    lon = request.args.get('lon', None)
    if ev_id and lat and lon:
        return json.dumps({"code": 0, "data": getEVClusters(float(lat), float(lon)), "message": "All nearby clusters"})
    else:
        return json.dumps({"code": 0, "data": [], "message": "Invalid Input"})


@app.route('/changeClusterStatus', methods=['POST', 'GET'])
def changeClusterStatus(): #Todo
    lat = request.args.get('lat', None)
    lon = request.args.get('lon', None)
    ev_lat = request.args.get('ev_lat', None)
    ev_lon = request.args.get('ev_lon', None)
    cluster_id = 1
    if cluster_id and ev_lat and ev_lon:
        changeClusterStatusforEV(cluster_id, ev_lat, ev_lon)
        return "1"
    return "0"


if __name__ == "__main__":
    start_socket()
    app.run(threaded=True)
