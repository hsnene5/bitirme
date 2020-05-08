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

$('#guided').on('click', function () {
    $.ajax({
        method: 'PUT',
        url: '/api/guided',
        contentType: 'application/json',
        data: JSON.stringify({ mode: 'GUIDED' }),
    })
        .done(function (msg) {
            console.log('sent guided mode')
        });
})

$('#auto').on('click', function () {
    $.ajax({
        method: 'PUT',
        url: '/api/auto',
        contentType: 'application/json',
        data: JSON.stringify({ mode: 'GUIDED' }),
    })
        .done(function (msg) {
            console.log('sent guided mode')
        });

})



var modal = document.getElementById("autoModePopup");
var span = document.getElementById("closeModal");


var closeModal = document.getElementById("closeModal");
// When the user clicks on <span> (x), close the modal
/*closeModal.onclick = function () {
    modal.style.display = "none";
}

// THINK ABOUT THAT FEATURE
// When the user clicks anywhere outside of the modal, close it
/*window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}*/