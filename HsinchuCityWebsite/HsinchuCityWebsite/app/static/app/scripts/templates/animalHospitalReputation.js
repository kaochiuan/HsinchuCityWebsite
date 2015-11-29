var map;
var dialog;
var infowindow; //對話視窗
var markerClusterer; //地圖markerculster
var markerClustererOpts = { gridSize: 50, maxZoom: 15 }; //cluster參數
var markerArray = [];
$(function () {
    initMap();
    dialog = $("#dialog");
    startToReputate();

    $("#startToReputate").button().click(startToReputate);
    //Responsive Google Map
    google.maps.event.addDomListener(window, 'resize', initMap);
    google.maps.event.addDomListener(window, 'load', initMap)
    //infowindow close listener
    google.maps.event.addListener(infowindow, 'closeclick', function () { });

    google.maps.event.addListener(map, 'zoom_changed', function () { infowindow.close(); });
});

function startToReputate() {
    BootstrapDialog.show({
        title: '新竹市動物醫院評比',
        message: dialog,
        buttons: [{
            label: '確定',
            cssClass: 'btn btn-default btn-3',
            action: function (dialogRef) {
                filterByConditions();
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
    return String.format("<div>動物醫院：{0}<br/>評比分數：{1}<br/></div>",
        data.name, data.reputation);
}

function filterByConditions() {
    var url = $.url("getReputationOfAnimalHospital");
    $.blockUI({ message: "正在評比新竹市所有動物醫院" });

    $.ajax({
        url: url,
        cache: false,
        type: 'POST',
        data: {},
        dataType: "json",
        success: function (data) {
            //put marker to google map
            if (data.status == "Success") {
                repData = data;
                markerArray.splice(0, markerArray.length);
                $.each(repData.reputation, function (index, reputation) {
                    var geoLatLng = new google.maps.LatLng(reputation.latitude, reputation.longitude);
                    var l_maker = googleMarkerCreator(geoLatLng, reputation.name, map, reputation);
                    markerArray.push(l_maker);
                    mapcenterBound.extend(geoLatLng);
                });
                map.fitBounds(mapcenterBound);
                markerClusterer = new MarkerClusterer(map, markerArray);
            }
            $.unblockUI({ message: "評比完成!!" });
        },
        error: function (data) {
            $.unblockUI({ message: "評比中斷!!" });
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