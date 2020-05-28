var marker2;
var map2;
function mainMap2() {


    var mapProp2 = {
        center: new google.maps.LatLng(0, 0),
        zoom: 19,
    };
    var iconBase = 'https://maps.google.com/mapfiles/kml/shapes/';
    map2 = new google.maps.Map(document.getElementById("guidedSelectMap"), mapProp2);
    map2.setMapTypeId(google.maps.MapTypeId.HYBRID);
    //infoWindow = new google.maps.InfoWindow;
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            var pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };

            //infoWindow.setPosition(pos);
            //infoWindow.setContent('Location found.');
            //infoWindow.open(map);
            map2.setCenter(pos);
            var user = { lat: position.coords.latitude, lng: position.coords.longitude };
            marker2 = new google.maps.Marker({ position: user, map: map2, icon: iconBase + 'man.png' })
        }, function () {
            handleLocationError(true, map2.getCenter());
        });
    } else {
        // Browser doesn't support Geolocation
        handleLocationError(false, map2.getCenter());
    }

}

$('#guidedSelectMapButton').on('click', function () {
    var elem = document.getElementById('guidedSelectMap');
    if (elem.style.display == "block") {
        elem.style.display = "none";
    } else {
        elem.style.display = "block";
    }
})

/*var marker;
var map;
function mainMap() {


    var mapProp = {
        center: new google.maps.LatLng(0, 0),
        zoom: 19,
    };
    var iconBase = 'https://maps.google.com/mapfiles/kml/shapes/';
    map = new google.maps.Map(document.getElementById("guidedSelectMap"), mapProp);
    map.setMapTypeId(google.maps.MapTypeId.HYBRID);
    google.maps.event.addListener(map, 'click', function (event) {
        var clickedLocation = event.LatLng;

        if (marker === false) {
            marker = new google.maps.Marker({
                position: clickedLocation,
                map: map,
                draggable: true
            });
            google.maps.event.addListener(marker, 'dragend', function (event) {
                markerLocation();
            });
        } else {
            marker.setPosition(clickedLocation);
        }
        markerLocation();
    });
}

function markerLocation() {
    var currentLocation = marker.getPosition();

    document.getElementById('guidedPointLat').value = currentLocation.lat();
    document.getElementById('guidedPointLon').value = currentLocation.lng();
}*/

    //infoWindow = new google.maps.InfoWindow;
    /*if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            var pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };

            //infoWindow.setPosition(pos);
            //infoWindow.setContent('Location found.');
            //infoWindow.open(map);
            map.setCenter(pos);
            var user = { lat: position.coords.latitude, lng: position.coords.longitude };
            marker = new google.maps.Marker({ position: user, map: map, icon: iconBase + 'man.png' })
        }, function () {
            handleLocationError(true, map.getCenter());
        });
    } else {
        // Browser doesn't support Geolocation
        handleLocationError(false, map.getCenter());
    }*/

