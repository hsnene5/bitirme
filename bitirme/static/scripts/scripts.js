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
    var modal = document.getElementById("autoModePopup");
    modal.style.display = "block";
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

var modal = document.getElementById("autoModePopup");
var span = document.getElementById("closeModal");


var closeModal = document.getElementById("closeModal");
// When the user clicks on <span> (x), close the modal
closeModal.onclick = function () {
    modal.style.display = "none";
}

// THINK ABOUT THAT FEATURE
// When the user clicks anywhere outside of the modal, close it
/*window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}*/