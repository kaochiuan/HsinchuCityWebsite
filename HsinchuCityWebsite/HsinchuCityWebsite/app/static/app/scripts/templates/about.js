$(document).ready(function () {
    $("#syncTemples").button().click(SyncTempleInfo);
    $("#syncCultureActivities").button().click(syncCultureInfo);
    $("#syncCityNews").button().click(syncCityNews);
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
            if (data.status == "Success")
                BootstrapDialog.show({
                    title: '求人不如求神',
                    message: "同步廟宇資訊成功",
                    buttons: [{
                        label: 'OK',
                        action: function (dialogRef) {
                            dialogRef.close();
                        }
                    }]
                });
        },
        error: function (data) {
        }
    });
}

function syncCultureInfo() {
    var url = $.url("syncCultureInfo");
    $.ajax({
        url: url,
        cache: false,
        type: 'POST',
        data: {},
        dataType: "json",
        success: function (data) {
            if (data.status == "Success")
                BootstrapDialog.show({
                    title: '藝文活動',
                    message: "同步當月藝文活動成功",
                    buttons: [{
                        label: 'OK',
                        action: function (dialogRef) {
                            dialogRef.close();
                        }
                    }]
                });
        },
        error: function (data) {
        }
    });
}

function syncCityNews() {
    var url = $.url("syncCityNews");
    $.ajax({
        url: url,
        cache: false,
        type: 'POST',
        data: {},
        dataType: "json",
        success: function (data) {
            if (data.status == "Success")
                BootstrapDialog.show({
                    title: '市政新聞',
                    message: "同步市政新聞成功",
                    buttons: [{
                        label: 'OK',
                        action: function (dialogRef) {
                            dialogRef.close();
                        }
                    }]
                });
        },
        error: function (data) {
        }
    });
}
