# DyReTra
### Dynamic Real-time Traffic Control System

Urban population in India is on a rise, and the time is not far away in the future that the traffic will be a huge problem to deal with. In fact major cities like Mumbai, Delhi and Bangalore are already facing it. There is a need of a smart solution, with minimum use of resources so that they can be accommodated in present infrastructure as well. Hence, we propose an idea that is purely based on analysis of Google Maps to detect and handle the traffic density. The core of the idea lies on Image Processing of the already existing Traffic API provided by Google. Google Traffic API provides the real-time data of the traffic conditions for any given coordinates, which gives color-coded traffic density data, which can be further processed to analyze the traffic flow at a given traffic junction and hence, the traffic lights can be dynamically controlled to regulate the traffic. This system works to make sure that there is not and uneven distribution of “Wait Time” and therefore uneven accumulation of traffic at a junction. The idea when centralized for a huge city with multiple traffic junctions can act as a synchronized system, which can also help in fluid movement of High Priority Vehicles/Emergency Vehicles.

## Built With

* [Flask](http://flask.pocoo.org/) - The python web framework used

## To run development server
* Install application as a python package in Virtual Environment - `pip install --editable .`
* export FLASK_APP=DyReTra
* export FLASK_DEBUG=true
* flask run
