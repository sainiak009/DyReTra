import googlemaps
import uuid
from flask_restful import Resource, Api, reqparse
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from datetime import datetime

from config import app
from config_values import GOOGLE_KEY
api = Api(app)

# # Congigurations
gmaps = googlemaps.Client(key=GOOGLE_KEY)

# Parameters to get a path
DirectionsParser = reqparse.RequestParser(bundle_errors=True)
DirectionsParser.add_argument('origin', type=str, required=True)
DirectionsParser.add_argument('destination', type=str, required=True)
# Parameters to get traffic details
MapTrafficParser = reqparse.RequestParser(bundle_errors=True)
MapTrafficParser.add_argument('latitude', type=float, required=True)
MapTrafficParser.add_argument('longitude', type=float, required=True)


class getDirectionsEV(Resource):
    def post(self):
        args = DirectionsParser.parse_args()
        now = datetime.now()
        directions = gmaps.directions(args['origin'], args['destination'], mode="transit", departure_time=now)
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
            isrunning = 0  # UNUSED
            driver.close()
            return "Exception has been thrown. " + str(ex)

        # setting file name for snapshot
        addr = str(datetime.now())
        addr = addr + '-' + str(uuid.uuid4())[:5]
        path = 'trafficSnaps/' + addr + '.png'
        driver.save_screenshot(path)
        driver.quit()
        return path


api.add_resource(getMapSnap, '/getMapSnap')
