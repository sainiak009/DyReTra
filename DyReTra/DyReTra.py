from config_values import *
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask_restful import Resource, Api, reqparse
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import googlemaps, uuid
from datetime import datetime
from datetime import datetime

app = Flask(__name__)
app.config.from_object(__name__)
api = Api(app)

# Congigurations

gmaps = googlemaps.Client(key=GOOGLE_KEY)
app.config.update(
    DEBUG=DEBUG,
    SECRET_KEY=SECRET_KEY
)


# All APIs will go here

# Parameters to get a path
DirectionsParser = reqparse.RequestParser(bundle_errors=True)
DirectionsParser.add_argument('origin', type=str, required=True)
DirectionsParser.add_argument('destination', type=str, required=True)
#parameters to get traffic details
MapTrafficParser = reqparse.RequestParser(bundle_errors=True)
MapTrafficParser.add_argument('latitude', type=float, required=True)
MapTrafficParser.add_argument('longitude', type=float, required=True)

class getDirectionsEV(Resource):
	def post(self):		
		args = DirectionsParser.parse_args()
		now = datetime.now()
		directions = gmaps.directions(args['origin'],args['destination'],mode="transit",departure_time=now)
		return directions

api.add_resource(getDirectionsEV, '/getDirectionsEV')


# API to get snapshot of traffic junction
class getMapSnap(Resource):
	def post(self):
		# Arguments parsing
		args = MapTrafficParser.parse_args()
		# Setting Proxy
		PROXY = "172.16.2.30:8080"
		chrome_options = webdriver.ChromeOptions()
		chrome_options.add_argument('--proxy-server=%s' % PROXY)
		chrome_options.add_argument('--proxy-bypass-list=%s' % "127.0.0.1*;localhost*")

		# Browsing page
		driver = webdriver.Chrome(chrome_options=chrome_options)
		try:
			driver.set_page_load_timeout(20)
			request_url = 'http://127.0.0.1:5000/trafficSnap/' + str(args['latitude']) + '/' + str(args['longitude'])
			driver.get(request_url)
		except TimeoutException as ex:
			isrunning = 0
			driver.close()
			return "Exception has been thrown. " + str(ex)

		# setting file name for snapshot
		addr = str(datetime.now())
		addr = addr + '-' + str(uuid.uuid4())[:5]
		path = 'trafficSnaps/'+addr + '.png'
		driver.save_screenshot(path) 
		driver.quit()
		return path

api.add_resource(getMapSnap, '/getMapSnap')

# All functions will go here 
@app.route('/')
def hello_world():
	return 'Hello, World!'


@app.route('/trafficSnap/<lat>/<lon>') # To generate traffic layers
def traffic_snap(lat, lon):
	return render_template('traffic_layer.html', latitude=lat, longitude=lon)

if __name__ == "__main__":
    app.run(threaded=True)