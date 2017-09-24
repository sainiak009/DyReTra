from config import app
from sockets import run as start_socket
# from tasks import run as start_scheduler
from simulator import simulateCluster, run as start_scheduler
from flask import render_template, request
from config_values import GOOGLE_KEY
from api import *

api = Api(app)

# All Api routes will go here
api.add_resource(getDirectionsEV, '/getDirectionsEV')
api.add_resource(getMapSnap, '/getMapSnap')


# All general routes will go here
@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/signal')
def traffic_signal():
    return render_template('traffic_signal.html')


@app.route('/start_cluster_simulation', methods=['POST', 'GET'])
def start_cluster_simulator():
    print(request.args.get('cluster_id', None))
    simulateCluster(cluster_id=request.args.get('cluster_id', None))
    return request.args.get('cluster_id', 'Hola')


@app.route('/trafficSnap/<lat>/<lon>')  # To generate traffic layers
def traffic_snap(lat, lon):
    return render_template('traffic_layer.html', latitude=lat, longitude=lon)


@app.route('/EVSimulator')	 # Emergency Vehicles Simulations
def EV_simulator():
    return render_template('ev_simulation.html', GOOGLE_KEY=GOOGLE_KEY)


if __name__ == "__main__":
    start_socket()
    start_scheduler()
    app.run(threaded=True)
