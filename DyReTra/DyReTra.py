import googlemaps

from datetime import datetime, timedelta
from random import randint

from config import app
from sockets import run as start_socket
# from tasks import run as start_scheduler
from simulator import simulateCluster, run as start_scheduler
from flask import render_template, request

# app = Flask(__name__)
# app.config.from_object(__name__)
# app.config.update(
#     DEBUG=DEBUG,
#     SECRET_KEY=SECRET_KEY
# )
# socketio = SocketIO(app)

# api = Api(app)

# # Congigurations

# gmaps = googlemaps.Client(key=GOOGLE_KEY)


# # All APIs will go here

# parser = reqparse.RequestParser()	# Initiating arguments parser
# parser.add_argument('origin', type=str)
# parser.add_argument('destination', type=str)

# class getDirectionsEV(Resource):
# 	def post(self):
# 		args = parser.parse_args()
# 		now = datetime.now()
# 		directions = gmaps.directions(args['origin'],args['destination'],mode="transit",departure_time=now)
# 		return directions

# api.add_resource(getDirectionsEV, '/getDirectionsEV')


# def emit_state(tl_id, cluster_id):
# 	emit('cluster-response', {"data": tl_id + " : " + str(run_time)}, room=cluster_id)

# def _simulate_cluster(cluster_id, tl_id):
# 	print("++++ here ++++")
# 	run_time = (datetime.now() + timedelta(minutes=randint(1,3) + 1))
# 	run_time = run_time.strftime("%Y-%m-%d %H:%M:%S")
# 	schedule.add_job(emit_state, 'date', run_date=run_time)


# def all_job_listener(event):
# 	if event.exception:
# 		# Log this and take necessary action
# 		print("Job Failed")
# 	else:
# 		print("Job Successful")
# 		if isinstance(event, JobExecutionEvent):



# All functions will go here 
@app.route('/')
def hello_world():
    # return "hi"
    return render_template('index.html')

@app.route('/start_cluster_simulation', methods=['POST', 'GET'])
def start_cluster_simulator():
	print(request.args.get('cluster_id', None))
	simulateCluster(cluster_id=request.args.get('cluster_id', None))
	return request.args.get('cluster_id', 'Hola')

if __name__ == "__main__":
	start_socket()
	start_scheduler()