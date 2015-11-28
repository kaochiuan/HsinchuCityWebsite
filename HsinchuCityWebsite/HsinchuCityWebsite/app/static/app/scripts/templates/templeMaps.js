var map;
var dialog;
var infowindow; //對話視窗
var markerClusterer; //地圖markerculster
var markerClustererOpts = { gridSize: 50, maxZoom: 15 }; //cluster參數
var markerArray = [];
$(function () {
    initMap();
    dialog = $("#dialog");

    templesFilter();
    $("#templesFilter").button().click(templesFilter);

    $("#regions").selectmenu().addClass("overflow");
    $("#belief").selectmenu().addClass("overflow");
    $("#masterGods").selectmenu().addClass("overflow");
    //Responsive Google Map
    google.maps.event.addDomListener(window, 'resize', initMap);
    google.maps.event.addDomListener(window, 'load', initMap)
    //infowindow close listener
    google.maps.event.addListener(infowindow, 'closeclick', function () { });

    google.maps.event.addListener(map, 'zoom_changed', function () { infowindow.close(); });
});

function templesFilter() {
    markerArray.splice(0, markerArray.length);
    initMap();
    BootstrapDialog.show({
        title: '求人不如求神',
        message: dialog,
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
}
function removeClickEvent() {
    google.maps.event.removeListener(clickEvent);
}
function googleMarkerCreator(_latlng, _title, _map, data) {
    var _Marker = new MarkerWithLabel({
        id: data.name,
        position: _latlng,
        flat: true,
        map: _map,
        draggable: false,
        labelContent: _title,
        labelAnchor: new google.maps.Point(20, 0),
        labelClass: "fontEffect",
        labelInBackground: true
    });
    _Marker.customInfo = data;
    google.maps.event.addListener(_Marker, 'click', mapMarkerTrigger);
    return _Marker;
}

function mapMarkerTrigger() {
    var marker = this;
    OpenInfo(marker);
}

function OpenInfo(marker) {
    //將marker放到全域
    if (typeof (marker) != "undefined") {
        infowindow.close();
        var data = marker.customInfo;
        var contents = GetInfoWindowHtml(data);
        infowindow.setContent(contents);
        if (map.getZoom() < 15) { map.setZoom(15); }
        map.setCenter(marker.getPosition());
        infowindow.open(map, marker);
    }
}

function GetInfoWindowHtml(data) {
    return String.format("<div>寺廟：{0}<br/>主祀神像：{1}<br/>地址：{2}<br/></div>", data.name, data.masterGod, data.address);
}

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
            //put marker to google map
            if (data.status == "Success") {
                templeData = data;
                markerArray.splice(0, markerArray.length);
                $.each(templeData.templeInfo, function (index, temple) {
                    var templeItem = temple.fields;
                    var geoLatLng = new google.maps.LatLng(templeItem.latitude, templeItem.longitude);
                    var l_maker = googleMarkerCreator(geoLatLng, templeItem.name, map, templeItem);
                    markerArray.push(l_maker);
                    mapcenterBound.extend(geoLatLng);
                });
                map.fitBounds(mapcenterBound);
                markerClusterer = new MarkerClusterer(map, markerArray);
            }
        },
        error: function (data) {
        }
    });
}

function initMap() {
    var myOptions = {
        zoom: 7,
        center: new google.maps.LatLng(24.801929, 120.971686),
        streetViewControl: true,
        scaleControl: true,
        zoomControl: true,
        zoomControlOptions: {
            position: google.maps.ControlPosition.TOP_CENTER,
            style: google.maps.ZoomControlStyle.LARGE
        },
        draggableCursor: 'crosshair'
    };

    map = new google.maps.Map(document.getElementById('map-canvas'), myOptions);

    mapcenterBound = new google.maps.LatLngBounds(null, null);
    infowindow = new google.maps.InfoWindow({ content: "", maxWidth: 600 });

    // avoid the map to clear all markers
    if (markerArray.length > 0) {
        var tempArray = [];
        $.each(markerArray, function (index, rep) {
            var geoLatLng = new google.maps.LatLng(rep.customInfo.latitude, rep.customInfo.longitude);
            var l_maker = googleMarkerCreator(geoLatLng, rep.customInfo.name, map, rep.customInfo);
            mapcenterBound.extend(geoLatLng);
            tempArray.push(l_maker);
        });
        markerArray.splice(0, markerArray.length);
        markerArray = tempArray;
        map.fitBounds(mapcenterBound);
        markerClusterer = new MarkerClusterer(map, markerArray);
    }
}