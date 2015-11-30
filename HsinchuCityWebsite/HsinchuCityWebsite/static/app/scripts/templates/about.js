$(document).ready(function () {
    $("#syncTemples").button().click(SyncTempleInfo);
    $("#syncCultureActivities").button().click(syncCultureInfo);
    $("#syncCityNews").button().click(syncCityNews);
    $("#animalHospitalReputation").button().click(getReputationOfAnimalHospital);
    
});

function getReputationOfAnimalHospital() {
    var url = $.url("syncReputationOfAnimalHospital");
    $.blockUI({ message: "正在評比新竹市所有動物醫院" });
    $.ajax({
        url: url,
        cache: false,
        type: 'POST',
        data: {},
        dataType: "json",
        success: function (data) {
            if (data.status == "Success") {
                $.unblockUI({ message: "評比完成!!" });
                BootstrapDialog.show({
                    title: '動物醫院評比',
                    message: "同步評比資訊, 並寫入資料庫成功",
                    buttons: [{
                        label: 'OK',
                        action: function (dialogRef) {
                            dialogRef.close();
                        }
                    }]
                });
            } else {
                $.unblockUI({ message: "評比過程有錯誤發生，請重新評比!!" });
                BootstrapDialog.show({
                    title: '動物醫院評比',
                    message: "取得評比失敗",
                    buttons: [{
                        label: 'OK',
                        action: function (dialogRef) {
                            dialogRef.close();
                        }
                    }]
                });
            }
        },
        error: function (data) {
        }
    });
}

function SyncTempleInfo() {
    var url = $.url("syncTempleInfo");
    $.ajax({
        url: url,
        cache: false,
        type: 'POST',
        data: {},
        dataType: "json",
        success: function (data) {
            if (data.status == "Success") {
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
            } else {
                BootstrapDialog.show({
                    title: '求人不如求神',
                    message: "同步廟宇資訊失敗",
                    buttons: [{
                        label: 'OK',
                        action: function (dialogRef) {
                            dialogRef.close();
                        }
                    }]
                });
            }
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
            if (data.status == "Success") {
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
            } else {
                BootstrapDialog.show({
                    title: '藝文活動',
                    message: "同步當月藝文活動失敗",
                    buttons: [{
                        label: 'OK',
                        action: function (dialogRef) {
                            dialogRef.close();
                        }
                    }]
                });
            }
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
            if (data.status == "Success") {
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
            } else {
                BootstrapDialog.show({
                    title: '市政新聞',
                    message: "同步市政新聞失敗",
                    buttons: [{
                        label: 'OK',
                        action: function (dialogRef) {
                            dialogRef.close();
                        }
                    }]
                });
            }
        },
        error: function (data) {
        }
    });
}
