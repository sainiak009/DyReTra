# DyReTra
### Dynamic Real-time Traffic Control System

Urban population in India is on a rise, and the time is not far away in the future that the traffic will be a huge problem to deal with. In fact major cities like Mumbai, Delhi and Bangalore are already facing it. There is a need of a smart solution, with minimum use of resources so that they can be accommodated in present infrastructure as well. Hence, we propose an idea that is purely based on analysis of Google Maps to detect and handle the traffic density. The core of the idea lies on Image Processing of the already existing Traffic API provided by Google. Google Traffic API provides the real-time data of the traffic conditions for any given coordinates, which gives color-coded traffic density data, which can be further processed to analyze the traffic flow at a given traffic junction and hence, the traffic lights can be dynamically controlled to regulate the traffic. This system works to make sure that there is not and uneven distribution of “Wait Time” and therefore uneven accumulation of traffic at a junction. The idea when centralized for a huge city with multiple traffic junctions can act as a synchronized system, which can also help in fluid movement of High Priority Vehicles/Emergency Vehicles.

## Built With

* [Flask](http://flask.pocoo.org/) - The python web framework used
* [Flask-RESTful](http://flask-restful.readthedocs.io/en/latest/) - Flask extention for building RESTful APIs
* [Flask-SocketIO](https://flask-socketio.readthedocs.io/en/latest/) - Low latency bi-directional communications between the clients and the server
* [googlemaps](https://github.com/googlemaps/google-maps-services-python) - Python client library for Google Maps API Web Services
* [Maps JavaScript API](https://developers.google.com/maps/documentation/javascript/) - API to render maps on frontend
* [OpenCV-Python](https://opencv-python-tutroals.readthedocs.io/en/latest/) - Python wrapper for the original OpenCV 
* [Selenium-Python](http://selenium-python.readthedocs.io/) - Headless browser
* [MongoDB](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/) - NoSQL database

## To run development server
### Install virtualenv
```
sudo apt-get install python-pip python-dev build-essentia
sudo pip install virtualenv virtualenvwrapper
sudo pip install --upgrade pip

# Create a backup of your .bashrc file
cp ~/.bashrc ~/.bashrc-org

# Be careful with this command
printf '\n%s\n%s\n%s' '# virtualenv' 'export WORKON_HOME=~/virtualenvs' \
'source /usr/local/bin/virtualenvwrapper.sh' >> ~/.bashrc

source ~/.bashrc

mkdir -p $WORKON_HOME

mkvirtualenv -p python3 dyretra
```


### Install and Run MongoDB server
[Install and Run MongoDB](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/)

### Install requirements and run server
```
source start.sh
```