var map;
var dialog;

$(function () {
    initMap();

    BootstrapDialog.show({
        title: '求人不如求神',
        message: $("#dialog"),
        buttons: [{
            label: 'OK',
            action: function (dialogRef) {
                filterByConditions();
                dialogRef.close();
            }
        }, {
            label: 'Abort',
            action: function (dialogRef) {
                dialogRef.close();
            }
        }]
    });

    $("#regions").selectmenu().addClass("overflow");
    $("#belief").selectmenu().addClass("overflow");
    $("#masterGods").selectmenu().addClass("overflow");

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