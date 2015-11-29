$(document).ready(function () {
    $("#getTopNews").button().click(getTopNews);
});

function getTopNews() {
    var url = $.url("getTop10News");
    $.ajax({
        url: url,
        cache: false,
        type: 'POST',
        data: {},
        dataType: "json",
        success: function (data) {
            if (data.status == "Success") {
                news = [];
                $.each(data.news, function (index, temple) {
                    var newsItem = temple.fields;
                    news.push(newsItem);
                });
                BootstrapDialog.show({
                    title: '市府新聞',
                    message: cityNewsDashboard(news),
                    buttons: [{
                        label: '確定',
                        cssClass: 'btn btn-default btn-3',
                        action: function (dialogRef) {
                            dialogRef.close();
                        }
                    }]
                });
            } else {
                BootstrapDialog.show({
                    title: '市府新聞',
                    message: "市府新聞取得失敗",
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


function cityNewsDashboard(data) {
    var result = "";
    $.each(data, function (index, item) {
        result += String.format("<div class='panel panel-default'><div class='panel-heading'>{0}<br/>發布日期：{1}</div> <div class='panel-body'>{2}</div></div>",
      item.type, item.publishDate, item.content);
    });
    return result;
}
