/*!
    * Start Bootstrap - SB Admin v6.0.0 (https://startbootstrap.com/templates/sb-admin)
    * Copyright 2013-2020 Start Bootstrap
    * Licensed under MIT (https://github.com/BlackrockDigital/startbootstrap-sb-admin/blob/master/LICENSE)
    */



    /*(function($) {
    "use strict";

    // Add active state to sidbar nav links
    var path = window.location.href; // because the 'href' property of the DOM element is the absolute path
        $("#layoutSidenav_nav .sb-sidenav a.nav-link").each(function() {
            if (this.href === path) {
                $(this).addClass("active");
            }
        });

    // Toggle the side navigation
    $("#sidebarToggle").on("click", function(e) {
        e.preventDefault();
        $("body").toggleClass("sb-sidenav-toggled");
    });

    

    
})(jQuery);*/

//var map = new ol.Map({
//    // controls: [],
//    // interactions : ol.interaction.defaults({
//    //   doubleClickZoom: false,
//    //   dragZoom: false,
//    //   keyboardZoom: false,
//    //   mouseWheelZoom: false,
//    //   pinchZoom: false,
//    // }),
//    target: 'googleMap',
//    renderer: 'canvas', // Force the renderer to be used
//    layers: [
//        new ol.layer.Tile({
//            source: new ol.source.BingMaps({
//                key: 'AnGHr16zmRWug0WA8mJKrMg5g6W4GejzGPBdP-wQ4Gqqw-yHNqsHmYPYh1VUOR1q',
//                imagerySet: 'AerialWithLabels',
//                // imagerySet: 'Road',
//            })
//        })
//    ],
//    view: new ol.View({
//        center: ol.proj.transform([39.9853521, 32.6448407], 'EPSG:4326', 'EPSG:3857'),
//        zoom: 18
//    })
//});

//var globmsg = null;

//var source = new EventSource('/api/sse/state');
//source.onmessage = function (event) {
//    var msg = JSON.parse(event.data);
//    if (!globmsg) {
//        console.log('FIRST', msg);
//        $('body').removeClass('disabled')
//        map.getView().setCenter(ol.proj.transform([msg.lon, msg.lat], 'EPSG:4326', 'EPSG:3857'));
//    }
//    globmsg = msg;

//    //$('#header-state').html('<b>Armed:</b> ' + msg.armed + '<br><b>Mode:</b> ' + msg.mode + '<br><b>Altitude:</b> ' + msg.alt.toFixed(2))
//    //$('#header-arm').prop('disabled', msg.armed);

//    //overlay.setPosition(ol.proj.transform([msg.lon, msg.lat], 'EPSG:4326', 'EPSG:3857'));
//    //$(overlay.getElement()).find('.heading').css('-webkit-transform', 'rotate(' + ((msg.heading) + 45) + 'deg)')
//};

//$('#header-center').on('click', function () {
//    map.getView().setCenter(ol.proj.transform([globmsg.lon, globmsg.lat], 'EPSG:4326', 'EPSG:3857'));
//})

var marker;
var map;
function mainMap() {
   
   
    var mapProp = {
        center: new google.maps.LatLng(0, 0),
        zoom: 19,
    };
    map = new google.maps.Map(document.getElementById("googleMap"), mapProp);
    map.setMapTypeId(google.maps.MapTypeId.HYBRID);
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
            map.setCenter(pos);
            var uluru = { lat: position.coords.latitude, lng: position.coords.longitude };
            marker = new google.maps.Marker({ position: uluru, map: map })
        }, function () {
            handleLocationError(true, map.getCenter());
        });
    } else {
        // Browser doesn't support Geolocation
        handleLocationError(false, map.getCenter());
    }

}

$('.popover-dismiss').popover({
    trigger: 'focus'
})

$(function () {
    $('[data-toggle="popover"]').popover()
})

$('#arm').on('click', function () {
    $.ajax({
        method: 'PUT',
        url: '/api/arm',
        contentType: 'application/json',
        data: JSON.stringify({ arm: true }),
    })
        .done(function (msg) {
            console.log('sent arming message')
        });
    document.getElementById("arm").innerHTML="armed";
})

$('#simulation').on('click', function () {
    $.ajax({
        method: 'PUT',
        url: '/api/simulation',
        contentType: 'application/json',
        data: JSON.stringify({ arm: true }),
    })
        .done(function (msg) {
            console.log('sent arming message')
        });
})

$('#guidedStart').on('click', function () {
    var dataY = {
        altitude : document.getElementById('guidedAlt').value,
        velocity : document.getElementById('guidedVel').value
        //pointLat: document.getElementById('guidedPointLat').value,
        //pointLon: document.getElementById('guidedPointLon').value
    };
    //console.log(altitude)
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
    //var altitude = document.getElementById('autoAlt').value;
    //var velocity = document.getElementById('autoVel').value;
    //var point1Lan = document.getElementById('autoPoint1Lan').value;
    //var point1Lon = doucument.getElementById('autoPoint1Lon').value;
    //var point2Lan = document.getElementById('autoPoint2Lan').value;
    //var point2Lon = doucument.getElementById('autoPoint2Lon').value;
    var dataX = {
        altitude : document.getElementById('autoAlt').value,
        velocity : document.getElementById('autoVel').value,
        point1Lan : document.getElementById('autoPoint1Lat').value,
        point1Lon : document.getElementById('autoPoint1Lon').value,
        point2Lan : document.getElementById('autoPoint2Lat').value,
        point2Lon : document.getElementById('autoPoint2Lon').value
    };
    //console.log(altitude)
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
    var ele = document.getElementsByName('cancelradio'); 
    var selected;
              
    for(i = 0; i < ele.length; i++) { 
        if(ele[i].checked) 
            selected = ele[i].checked;
    } 

    console.log(selected)
    $.ajax({
        method: 'PUT',
        url: '/api/cancel',
        contentType: 'application/json',
        data: JSON.stringify({ selected }),
    })
         .done(function (msg) {
             console.log('sent cancel mode')
         });

})

var globmsg = null;

var source = new EventSource('/api/sse/state');
source.onmessage = function (event) {
    var msg = JSON.parse(event.data);

    $('#header-state').html('<b>Armed:</b> ' + msg.armed + '<br><b>Mode:</b> ' + msg.mode + '<br><b>Altitude:</b> ' + msg.alt.toFixed(2))
    var uluru = { lat: msg.lat, lng: msg.lon };
    var point1 = msg.point1;
    var latlng = new google.maps.LatLng(msg.lat, msg.lon);
    map.setCenter(latlng);
    marker.setPosition(latlng);
    var marker2 = new google.maps.Marker({ point1, map: map })
}