$(document).ready(function () {
    $("#syncTemples").button().click(SyncTempleInfo);
});

function SyncTempleInfo() {
    var url = $.url("syncTempleInfo");
    $.ajax({
        url: url,
        cache: false,
        type: 'POST',
        data: {},
        dataType: "json",
        success: function (data) {
        },
        error: function (data) {
        }
    });
}
