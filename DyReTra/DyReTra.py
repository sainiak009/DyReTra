from .config_values import *
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask_restful import Resource, Api, reqparse
import googlemaps
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

parser = reqparse.RequestParser()	# Initiating arguments parser
parser.add_argument('origin', type=str)
parser.add_argument('destination', type=str)

class getDirectionsEV(Resource):
	def post(self):
		args = parser.parse_args()
		now = datetime.now()
		directions = gmaps.directions(args['origin'],args['destination'],mode="transit",departure_time=now)
		return directions

api.add_resource(getDirectionsEV, '/getDirectionsEV')



# All functions will go here 
@app.route('/')
def hello_world():
    return 'Hello, World!'