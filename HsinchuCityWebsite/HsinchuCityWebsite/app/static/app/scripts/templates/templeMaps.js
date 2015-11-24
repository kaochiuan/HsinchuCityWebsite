var map;
var dialog;

$(function () {
    initMap();

    dialog = $("#dialog").dialog({ modal: true });
});

function initMap() {
    var myOptions = {
        zoom: 10,
        center: new google.maps.LatLng(24.801929, 120.971686),
        streetViewControl: false,
        scaleControl: true,
        zoomControl: true,
        zoomControlOptions: {
            position: google.maps.ControlPosition.TOP_CENTER,
            style: google.maps.ZoomControlStyle.LARGE
        },
        draggableCursor: 'crosshair'
    };

    map = new google.maps.Map(document.getElementById('map-canvas'), myOptions);
}