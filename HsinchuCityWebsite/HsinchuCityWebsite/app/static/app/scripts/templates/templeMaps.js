var map;
var dialog;

$(function () {
    initMap();

    dialog = $("#dialog").dialog({ modal: true });
    $("#regions").selectmenu().addClass("overflow");
    $("#belief").selectmenu().addClass("overflow");
    $("#masterGods").selectmenu().addClass("overflow");

    $("#filterBtn").button().click(filterByConditions);

});

function filterByConditions() {
    var region = $('#regions option:selected').val();
    var belief = $('#belief option:selected').val();

    var url = $.url("filterTemple");
    $.ajax({
        url: url,
        cache: false,
        type: 'POST',
        data: { region: region, belief: belief },
        dataType: "json",
        success: function (data) {
        },
        error: function (data) {
        }
    });
}

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