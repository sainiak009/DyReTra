import googlemaps
import uuid
from flask_restful import Resource, reqparse
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from datetime import datetime

# from config import app
from config_values import GOOGLE_KEY


# Congigurations
gmaps = googlemaps.Client(key=GOOGLE_KEY)

# Parameters to get a path
DirectionsParser = reqparse.RequestParser(bundle_errors=True)
DirectionsParser.add_argument('origin_lat', type=float, required=True)
DirectionsParser.add_argument('origin_lng', type=float, required=True)
DirectionsParser.add_argument('destination_lat', type=float, required=True)
DirectionsParser.add_argument('destination_lng', type=float, required=True)
# Parameters to get traffic details
MapTrafficParser = reqparse.RequestParser(bundle_errors=True)
MapTrafficParser.add_argument('latitude', type=float, required=True)
MapTrafficParser.add_argument('longitude', type=float, required=True)


# API to get path for EVs
class getDirectionsEV(Resource):
    def post(self):
        args = DirectionsParser.parse_args()
        now = datetime.now()
        origin = str(args['origin_lat']) + ',' + str(args['origin_lng'])
        destination = str(args['destination_lat']) + ',' + str(args['destination_lng'])
        directions = gmaps.directions(origin, destination, departure_time=now)
        return directions

#  API ot get traffic lights locations data (To be developed later after getting actual sufficient data)


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
            driver.close()
            return "Exception has been thrown. " + str(ex)

        # setting file name for snapshot
        addr = str(datetime.now())
        addr = addr + '-' + str(uuid.uuid4())[:5]
        path = 'trafficSnaps/' + addr + '.png'
        driver.save_screenshot(path)
        driver.quit()
        return path
