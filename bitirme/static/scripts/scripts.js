
var map2; //Will contain map object.
var marker2 = false; ////Has the user plotted their location marker? 

var simMap;
var simMarker = false;

//Function called to initialize / create the map.
//This is called when the page has loaded.
function guidedMap() {

    //The center location of our map.
    var centerOfMap = new google.maps.LatLng(52.357971, -6.516758);

    //Map options.
    var options = {
        //center: centerOfMap, //Set center.
        zoom: 13 //The zoom value.
    };

    //Create the map object.
    map2 = new google.maps.Map(document.getElementById('guidedSelectMap'), options);
    map2.setMapTypeId(google.maps.MapTypeId.HYBRID);
    //Listen for any clicks on the map.
    google.maps.event.addListener(map2, 'click', function (event) {
        //Get the location that the user clicked.
        var clickedLocation = event.latLng;
        //If the marker hasn't been added.
        if (marker2 === false) {
            //Create the marker.
            marker2 = new google.maps.Marker({
                position: clickedLocation,
                map: map2,
                draggable: true, //make it draggable
            });
            //Listen for drag events!
            google.maps.event.addListener(marker2, 'dragend', function (event) {
                markerLocation();
            });
        } else {
            //Marker has already been added, so just change its location.
            marker2.setPosition(clickedLocation);
        }
        //Get the marker's location.
        guidedMarkerLocation();
    });
}

function simulationMap() {

    //The center location of our map.
    var mapProp = {
        
        zoom: 14,
    };

    simMap = new google.maps.Map(document.getElementById("simulationSelectMap"), mapProp);
    simMap.setMapTypeId(google.maps.MapTypeId.HYBRID);
    //infoWindow = new google.maps.InfoWindow;

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            var pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };

            simMap.setCenter(pos);

            var user = { lat: position.coords.latitude, lng: position.coords.longitude };
            marker = new google.maps.Marker({ position: user, map: simMap, icon: iconBase + 'man.png' });
            simMarker = new google.maps.Marker({ position: user, map: simMap });
        }, function () {
            handleLocationError(true, simMap.getCenter());
        });
    } else {
        // Browser doesn't support Geolocation
        handleLocationError(false, simMap.getCenter());
    }
    google.maps.event.addListener(simMap, 'click', function (event) {
        //Get the location that the user clicked.
        var clickedLocation = event.latLng;
        //If the marker hasn't been added.
        if (simMarker === false) {
            //Create the marker.
            simMarker = new google.maps.Marker({
                position: clickedLocation,
                map: simMap,
                draggable: true, //make it draggable
            });
            //Listen for drag events!
            google.maps.event.addListener(simMarker, 'dragend', function (event) {
                 simulationMarkerLocation();
            });
        } else {
            //Marker has already been added, so just change its location.
            simMarker.setPosition(clickedLocation);
        }
        //Get the marker's location.
        simulationMarkerLocation();
    });
}

function guidedMarkerLocation() {
    //Get location.
    var currentLocation = marker2.getPosition();
    if (google.maps.geometry.spherical.computeDistanceBetween(currentLocation, rangeCircle.center) > rangeCircle.radius) {
        $('.alert').alert();
        
        marker2.setPosition(rangeCircle.center);
        return;
    }
    //Add lat and lng values to a field that we can save.
    $('#toast').toast('hide');
    document.getElementById('guidedPointLat').value = currentLocation.lat(); //latitude
    document.getElementById('guidedPointLon').value = currentLocation.lng(); //longitude
}

function simulationMarkerLocation() {
    var currentLocation = simMarker.getPosition();

    document.getElementById('simulationHomeLat').value = currentLocation.lat(); //latitude
    document.getElementById('simulationHomeLon').value = currentLocation.lng(); //longitude
}

function initMaps() {
    mainMap();
    guidedMap();
    simulationMap();
}

var iconBase = 'http://maps.google.com/mapfiles/kml/shapes/';
var marker;
var map;
function mainMap() {

    var mapProp = {
        center: new google.maps.LatLng(0, 0),
        zoom: 19,
    };

    var iconBase = 'https://maps.google.com/mapfiles/kml/shapes/';
    map = new google.maps.Map(document.getElementById("googleMap"), mapProp);
    map.setMapTypeId(google.maps.MapTypeId.HYBRID);
    //infoWindow = new google.maps.InfoWindow;
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            var pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };

            map.setCenter(pos);

            var user = { lat: position.coords.latitude, lng: position.coords.longitude };
            marker = new google.maps.Marker({ position: user, map: map, icon: iconBase + 'man.png' })
        }, function () {
            handleLocationError(true, map.getCenter());
        });
    } else {
        // Browser doesn't support Geolocation
        handleLocationError(false, map.getCenter());
    }

}

function selectNewLocation() {
    if (document.getElementById("secondPoint").style.display == 'none') {
        document.getElementById("exampleModalLongTitle2").style.display = 'block';
        document.getElementById("secondPoint").style.display = 'flex';
    }
    else if (document.getElementById("thirdPoint").style.display == 'none') {
        document.getElementById("exampleModalLongTitle3").style.display = 'block';
        document.getElementById("thirdPoint").style.display = 'flex';
    }
    else if (document.getElementById("fourthPoint").style.display == 'none') {
        document.getElementById("exampleModalLongTitle4").style.display = 'block';
        document.getElementById("fourthPoint").style.display = 'flex';
    }
}

function enableFlightModes(connectionMode)
{
    document.getElementById('auto').disabled = false;
    document.getElementById('guided').disabled = false;
}

function enableComponents(flightMode) {
    if (flightMode == 'guided') {
        document.getElementById('auto').disabled = true;
    } else if (flightMode == 'auto') {
        document.getElementById('guided').disabled = true;
    }
    document.getElementById('rtl').disabled = false;
    document.getElementById('land').disabled = false;
    document.getElementById('cancel').disabled = false;
}

$('.popover-dismiss').popover({
    trigger: 'hover'
})

$(function () {
    $('[data-toggle="popover"]').popover({
        trigger:'hover'
    });
})

$('#connect').on('click', function () {
    document.getElementById('simulation').disabled = true;
    $.ajax({
        method: 'PUT',
        url: '/api/arm',
        contentType: 'application/json',
        data: JSON.stringify({ arm: true }),
    })
        .done(function (msg) {
            console.log('sent arming message')
        });
    //document.getElementById("connect").innerHTML="armed";
})

$('#simulationStart').on('click', function () {
    document.getElementById('connect').disabled = true;
    enableFlightModes();
    var simMarkerLocation = simMarker.getPosition();
    var homeLocation = {
        lng: simMarkerLocation.lng(),
        lat: simMarkerLocation.lat(),
    };

    $('#simulation').prop("disabled", true);
    $('#simulation').html(
        '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...'
    );
    $("#spinner").css("display", "block");
    $.ajax({
        method: 'PUT',
        url: '/api/simulation',
        contentType: 'application/json',
        data: JSON.stringify({ homeLocation }),
        success: function () {
            $('#simulation').html("Simulation");
            $("#spinner").css("display", "none");
        }
    })
        .done(function (msg) {
            console.log('sent arming message');
        });
})

$('#guidedStart').on('click', function () {
    var guidedAltitude = document.getElementById('guidedAlt').value;
    var guidedVelocity = document.getElementById('guidedVel').value;
    var guidedPointLat = document.getElementById('guidedPointLat').value;
    var guidedPointLon = document.getElementById('guidedPointLon').value;
    var afterArrival = document.querySelector('input[name="guidedRadio"]:checked').value;
    
    if (guidedAltitude == "" && guidedVelocity == "") {
        alert("Altitude and Velocity parameters cannot be empty!");
        document.getElementById('guidedAlt').style["border"] = "2 px solid red";
        document.getElementById('guidedVel').style["background-color"] = "red";
        return false;
    }

    if (guidedAltitude == "") {
        alert("Altitude parameter cannot be empty!");
        document.getElementById('guidedAlt').style["background-color"] = "red";
        return false;
    }

    if (guidedVelocity == "") {
        alert("Velocity parameter cannot be empty!");
        document.getElementById('guidedVel').style["background-color"] = "red";
        return false;
    }

    var dataY = {
        altitude : document.getElementById('guidedAlt').value,
        velocity: document.getElementById('guidedVel').value,
        point1Lat: guidedPointLat,
        point1Lon: guidedPointLon,
        afterArrival: afterArrival
    };

    enableComponents('guided');
    var uluru = { lat: parseFloat(guidedPointLat), lng: parseFloat(guidedPointLon) };
    pointMarker = new google.maps.Marker({ position: uluru, map: map });

    $.ajax({
        method: 'PUT',
        url: '/api/guided',
        contentType: 'application/json',
        data: JSON.stringify({ dataY }),
    })
         .done(function (msg) {
             console.log('sent guided mode')
         });

})

$('#autoStart').on('click', function () {
    var dataX = {
        altitude : document.getElementById('autoAlt').value,
        velocity : document.getElementById('autoVel').value,
        point1Lat : document.getElementById('autoPoint1Lat').value,
        point1Lon : document.getElementById('autoPoint1Lon').value,
        point2Lat : document.getElementById('autoPoint2Lat').value,
        point2Lon: document.getElementById('autoPoint2Lon').value,
        point3Lat: document.getElementById('autoPoint3Lat').value,
        point3Lon: document.getElementById('autoPoint3Lon').value,
        point4Lat: document.getElementById('autoPoint4Lat').value,
        point4Lon: document.getElementById('autoPoint4Lon').value
    };

    $.ajax({
        method: 'PUT',
        url: '/api/auto',
        contentType: 'application/json',
        data: JSON.stringify({ dataX }),
    })
        .done(function (msg) {
            console.log('sent guided mode')
        });

})

$('#land').on('click', function () {
    $.ajax({
        method: 'PUT',
        url: '/api/land',
        contentType: 'application/json',
        data: JSON.stringify({ mode: 'LAND' }),
    })
        .done(function (msg) {
            console.log('sent landing mode')
       });

})

$('#loiter').on('click', function () {
    $.ajax({
        method: 'PUT',
        url: '/api/loiter',
        contentType: 'application/json',
        data: JSON.stringify({ mode: 'LOITER' }),
    })
        .done(function (msg) {
            console.log('sent loiter mode')
        });

})

$('#cancelStart').on('click', function () {

    var dataSelected = document.querySelector('input[name="cancelRadio"]:checked').value;

    $.ajax({
        method: 'PUT',
        url: '/api/cancel',
        contentType: 'application/json',
        data: JSON.stringify({ dataSelected }),
    })
         .done(function (msg) {
             console.log('sent cancel mode')
         });

})

$('#simulationSelectMapButton').on('click', function () {
    var elem = document.getElementById('simulationSelectMap');
    if (elem.style.display == "block") {
        elem.style.display = "none";
    } else {
        elem.style.display = "block";
    }
})

$('#simulationUserLocation').on('click', function () {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {

            var pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };

            simMap.setCenter(pos);

            if (simMarker != null) {
                simMarker.setPosition(pos);
            }
            
            document.getElementById('simulationHomeLat').value = pos.lat;
            document.getElementById('simulationHomeLon').value = pos.lng;
            
        }, function () {
            handleLocationError(true, simMap.getCenter());
        });
    } else {
        // Browser doesn't support Geolocation
        handleLocationError(false, simMap.getCenter());
    }
})


$('#guidedSelectMapButton').on('click', function () {
    var elem = document.getElementById('guidedSelectMap');
    if (elem.style.display == "block") {
        elem.style.display = "none";
        console.log("block")
    } else {
        elem.style.display = "block";
    }
})

var globmsg = null;
var droneMarker = new google.maps.Marker({ map: map, icon: iconBase + 'heliport.png' });
var rangeCircle = new google.maps.Circle({
    strokeColor: '#1ec904',
    strokeOpacity: 0.8,
    fill: false,
    strokeWeight: 2,
    map: map2,
    clickable: false,
    radius: 1500
});

var source = new EventSource('/api/sse/state');
source.onmessage = function (event) {
    var msg = JSON.parse(event.data);
    //console.log(msg.spinner);
    if (spinner = false) {

    }
    $('#header-state').html('<b>Vehicle:</b> ' + msg.vehicleState +'<br><b>Armed:</b> ' + msg.armed + '<br><b>Mode:</b> ' + msg.mode + '<br><b>Altitude:</b> ' + msg.alt.toFixed(2))
    var uluru = { lat: msg.lat, lng: msg.lon };
    var point1 = msg.point1;
    var latlng = new google.maps.LatLng(msg.lat, msg.lon);
    map.setCenter(latlng);
    map2.setCenter(latlng);
    map.setCenter(latlng);
    //droneMarker;
    rangeCircle.setCenter(latlng);
    droneMarker.setPosition(latlng);
    //var marker2 = new google.maps.Marker({ point1, map: map })
}

//google.maps.event.addDomListener(window, 'load', mainMap);