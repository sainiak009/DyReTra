// This will open instructions modal as soon as page loads
$('#myModal').modal('show');

$("#setOrigin").click(function() {
    var lat = $("#ev_lat").val();
    var lon = $("#ev_lon").val();
    initMap(lat, lon);
    console.log("EV Origin set")
});

trafficLights = []; // To store traffic lights coordinates to be rendered
var trafficLightsMarkers = []; // To store traffic light markers

// API Call to get traffic signals location data of given locality and make server aware of our movement
$("#sendDest").click(function() {
    console.log($("#ev_lat").val());
    console.log($("#ev_lon").val());
    $.ajax({
        url: '/getNearbyCluster',
        type: 'GET',
        data: {
            lat: $("#ev_lat").val(),
            lon: $("#ev_lon").val(),
            ev_id: 1
        },
        success: function(response) {
            var res_json = JSON.parse(response);
            res_json.data.forEach(function(item, index) {
                trafficLights.push({
                    lat: parseFloat(item.coordinates.lat),
                    lng: parseFloat(item.coordinates.lon)
                });
                console.log(trafficLights);
            });
        }
    });
    initMap($("#ev_lat").val(), $("#ev_lon").val(), $("#lat").val(), $("#lng").val());
});


// Function to create markers on google maps 
function createMarker(latlng, label, html) {
    var contentString = '<b>' + label + '</b><br>' + html;
    var marker = new google.maps.Marker({
        position: latlng,
        map: map,
        title: label,
        zIndex: Math.round(latlng.lat() * -100000) << 5
    });
    marker.myname = label;

    google.maps.event.addListener(marker, 'click', function() {
        infowindow.setContent(contentString);
        infowindow.open(map, marker);
    });
    return marker;
}


// Function to render map with given coordinate/coordinates
// It will render best path if both origin and desgtination coordinates are given 
function initMap(EV_origin_lat = 0, EV_origin_lng = 0, EV_dest_lat = 0, EV_dest_lng = 0) {
    var origin;

    //Setting Origin
    if (EV_origin_lng && EV_origin_lat) {
        origin = {
            lat: parseFloat(EV_origin_lat),
            lng: parseFloat(EV_origin_lng)
        };
    } else {
        origin = {
            lat: 22.5748516,
            lng: 88.40156619999993
        }; // If Origin not given setting it to Apollo Gleneagles Hospitals,Kolkata
    }

    // Setting Map
    map = new google.maps.Map(document.getElementById('map'), {
        center: origin,
        zoom: 17
    });

    //----------------------------------------------------------------------------------------------

    // Below code is to set up destination Search Box

    // Create the search box and link it to the UI element.
    var input = document.getElementById('pac-input');
    var searchBox = new google.maps.places.SearchBox(input);

    // Bias the SearchBox results towards current map's viewport.
    map.addListener('bounds_changed', function() {
        searchBox.setBounds(map.getBounds());
    });

    // Listen for the event fired when the user selects a prediction and retrieve
    // more details for that place.
    map.addListener('bounds_changed', function() {
        searchBox.setBounds(map.getBounds());
    });

    var markers = [];
    // Listen for the event fired when the user selects a prediction and retrieve
    // more details for that place.
    searchBox.addListener('places_changed', function() {
        var places = searchBox.getPlaces();

        if (places.length == 0) {
            return;
        }

        // If multiple locations selected, for each place, get the icon, name and location.
        var bounds = new google.maps.LatLngBounds();
        places.forEach(function(place) {
            if (!place.geometry) {
                console.log("Returned place contains no geometry");
                return;
            }

            $("#lat").val(place.geometry.location.lat());
            $("#lng").val(place.geometry.location.lng());
            // Create a marker for each place.
            markers.push(new google.maps.Marker({
                map: map,
                // icon: icon,
                label: 'B',
                title: place.name,
                position: place.geometry.location
            }));

            if (place.geometry.viewport) {
                // Only geocodes have viewport.
                bounds.union(place.geometry.viewport);
            } else {
                bounds.extend(place.geometry.location);
            }
        });
        map.fitBounds(bounds);
    });

    //----------------------------------------------------------------------------------------------


    // Setting map to Render Traffic layer
    var trafficLayer = new google.maps.TrafficLayer();
    trafficLayer.setMap(map);

    // Setting map to render directions
    directionsDisplay = new google.maps.DirectionsRenderer({
        map: map
    });

    //Set destination, origin and travel mode.
    if (EV_dest_lng && EV_dest_lat) {
        request = {
            destination: {
                lat: parseFloat(EV_dest_lat),
                lng: parseFloat(EV_dest_lng)
            },
            origin: origin,
            travelMode: 'DRIVING',
            drivingOptions: {
                departureTime: new Date(Date.now())
            }
        }

        // Pass the directions request to the directions service.
        directionsService = new google.maps.DirectionsService();
        directionsService.route(request, function(response, status) {
            if (status == 'OK') {
                // Display the route on the map.
                directionsDisplay.setDirections(response);
            }
        });

    } else {
        //Setting origin marker
        var EVMarker1 = new google.maps.Marker({
            position: origin,
            map: map,
            title: 'Ambulance',
            label: 'A'
        });
    }

    // Creating markers for Traffic lights
    trafficLights.forEach(function(item, index) {
        trafficLightsMarkers[index] = new google.maps.Marker({
            icon: "http://maps.google.com/mapfiles/ms/icons/red-dot.png",
            position: item,
            map: map,
            title: 'Traffic Light ' + (index + 1)
        });
    });

    //------------- Some useful funcitons taken from epoly.js API V3 ---------------------


    google.maps.event.addDomListener(window, "load", initMap);


    google.maps.LatLng.prototype.latRadians = function() {
        return this.lat() * Math.PI / 180;
    }

    google.maps.LatLng.prototype.lngRadians = function() {
        return this.lng() * Math.PI / 180;
    }


    // === A method which returns a GLatLng of a point a given distance along the path ===
    // === Returns null if the path is shorter than the specified distance ===
    google.maps.Polyline.prototype.GetPointAtDistance = function(metres) {
        // some awkward special cases
        if (metres == 0) return this.getPath().getAt(0);
        if (metres < 0) return null;
        if (this.getPath().getLength() < 2) return null;
        var dist = 0;
        var olddist = 0;
        for (var i = 1;
            (i < this.getPath().getLength() && dist < metres); i++) {
            olddist = dist;
            dist += google.maps.geometry.spherical.computeDistanceBetween(this.getPath().getAt(i), this.getPath().getAt(i - 1));
        }
        if (dist < metres) {
            return null;
        }
        var p1 = this.getPath().getAt(i - 2);
        var p2 = this.getPath().getAt(i - 1);
        var m = (metres - olddist) / (dist - olddist);
        return new google.maps.LatLng(p1.lat() + (p2.lat() - p1.lat()) * m, p1.lng() + (p2.lng() - p1.lng()) * m);
    }

    // === A method which returns the Vertex number at a given distance along the path ===
    // === Returns null if the path is shorter than the specified distance ===
    google.maps.Polyline.prototype.GetIndexAtDistance = function(metres) {
        // some awkward special cases
        if (metres == 0) return this.getPath().getAt(0);
        if (metres < 0) return null;
        var dist = 0;
        var olddist = 0;
        for (var i = 1;
            (i < this.getPath().getLength() && dist < metres); i++) {
            olddist = dist;
            dist += google.maps.geometry.spherical.computeDistanceBetween(this.getPath().getAt(i), this.getPath().getAt(i - 1));
        }
        if (dist < metres) {
            return null;
        }
        return i;
    }


};
// End of initMap functions


// To calculate and reder final path to be followed by Vehicle
function calcRoute() {
    directionsDisplay.setMap(null);

    // Creating poly lines variables for Vehicular Movement
    polyline = new google.maps.Polyline({
        path: [],
        strokeColor: '#FF0000',
        strokeWeight: 3
    });
    poly2 = new google.maps.Polyline({
        path: [],
        strokeColor: '#FF0000',
        strokeWeight: 3
    });
    // Create a renderer for directions and bind it to the map.
    var rendererOptions = {
        map: map
    }

    directionsDisplay = new google.maps.DirectionsRenderer(rendererOptions);

    var start = {
        lat: parseFloat($("#ev_lat").val()),
        lng: parseFloat($("#ev_lon").val())
    };
    var end = {
        lat: parseFloat($("#lat").val()),
        lng: parseFloat($("#lng").val())
    };
    var travelMode = google.maps.DirectionsTravelMode.DRIVING

    var request = {
        origin: start,
        destination: end,
        travelMode: travelMode
    };

    // Route the directions and pass the response to a
    // function to create markers for each step.
    directionsService.route(request, function(response, status) {
        if (status == google.maps.DirectionsStatus.OK) {
            directionsDisplay.setDirections(response);

            var bounds = new google.maps.LatLngBounds();
            var route = response.routes[0];
            startLocation = new Object();
            endLocation = new Object();

            // For each route, display summary information.
            var path = response.routes[0].overview_path;
            var legs = response.routes[0].legs;
            for (i = 0; i < legs.length; i++) {
                if (i == 0) {
                    startLocation.latlng = legs[i].start_location;
                    startLocation.address = legs[i].start_address;
                    // marker = google.maps.Marker({map:map,position: startLocation.latlng});
                    marker = createMarker(legs[i].start_location, "Vehicle", legs[i].start_address, "green");
                }
                endLocation.latlng = legs[i].end_location;
                endLocation.address = legs[i].end_address;
                var steps = legs[i].steps;
                for (j = 0; j < steps.length; j++) {
                    var nextSegment = steps[j].path;
                    for (k = 0; k < nextSegment.length; k++) {
                        polyline.getPath().push(nextSegment[k]);
                        bounds.extend(nextSegment[k]);
                    }
                }
            }

            polyline.setMap(map);
            map.fitBounds(bounds);
            map.setZoom(18);
            startAnimation(); // Initiating animation here
        }
    });
}



var step = 50; //  metres
var tick = 100; // milliseconds
var eol; // end of line
var lastVertex = 1;


//=============== animation functions ======================

// CREATING AND SETTING POLYLINES FOR VEHICULAR MOVEMENT
function updatePoly(d) {
    // Spawn a new polyline every 20 vertices, because updating a 100-vertex poly is too slow
    if (poly2.getPath().getLength() > 20) {
        poly2 = new google.maps.Polyline([polyline.getPath().getAt(lastVertex - 1)]);
    }

    if (polyline.GetIndexAtDistance(d) < lastVertex + 2) {
        if (poly2.getPath().getLength() > 1) {
            poly2.getPath().removeAt(poly2.getPath().getLength() - 1)
        }
        poly2.getPath().insertAt(poly2.getPath().getLength(), polyline.GetPointAtDistance(d));
    } else {
        poly2.getPath().insertAt(poly2.getPath().getLength(), endLocation.latlng);
    }
}

// CONTINUOS VEHICLE LOCATION IS SET HERE
function animate(d) {
    if (d > eol) {
        map.panTo(endLocation.latlng);
        marker.setPosition(endLocation.latlng);
        return;
    }
    var p = polyline.GetPointAtDistance(d);

    // HERE I AM CHECKING IF A TRAFFIC CLUSTER IS IN OUR VEHICLE'S RANGE
    // IF IN RANGE THEN REQUEST TO MAKE THE SIGNAL WILL BE SENT TO SERVER
    try {
        trafficLightsMarkers.forEach(function(item, index) {
            if (checkIfWithInDistance(polyline.GetPointAtDistance(d + 500).lat(), polyline.GetPointAtDistance(d + 500).lng(), trafficLights[index].lat, trafficLights[index].lng, 1)) {
                item.setIcon('http://maps.google.com/mapfiles/ms/icons/green-dot.png');
                // Sending signal that EV is about to reach this cluster
                $.ajax({
                    url: '/changeClusterStatus',
                    type: 'POST',
                    data: {
                        lat: trafficLights[index].lat,
                        lon: trafficLights[index].lng,
                        ev_lat: polyline.GetPointAtDistance(d).lat(),
                        ev_lon: polyline.GetPointAtDistance(d).lng()
                    },
                    success: function(response) {
                        console.log(response);
                    }
                });
            }
        });
    } catch (err) {;
    }
    map.panTo(p);
    marker.setPosition(p);
    updatePoly(d);
    timerHandle = setTimeout("animate(" + (d + step) + ")", tick);
}

// Function to start simulation
function startAnimation() {
    eol = google.maps.geometry.spherical.computeLength(polyline.getPath());
    map.setCenter(polyline.getPath().getAt(0));
    poly2 = new google.maps.Polyline({
        path: [polyline.getPath().getAt(0)],
        strokeColor: "#0000FF",
        strokeWeight: 10
    });
    setTimeout("animate(50)", 2000); // Allow time for the initial map display
}


// This function will tell if given coordinates are within a distance "d" from origin coordinates
function checkIfWithInDistance(origin_lat, origin_lng, point_lat, point_lng, d) { // Distance in kilometer
    var distance = Math.acos(Math.sin(origin_lat) * Math.sin(point_lat) + Math.cos(origin_lat) * Math.cos(point_lat) * Math.cos(point_lng - (origin_lng))) * 6371;

    if (distance <= d) return true;
    else false;
}