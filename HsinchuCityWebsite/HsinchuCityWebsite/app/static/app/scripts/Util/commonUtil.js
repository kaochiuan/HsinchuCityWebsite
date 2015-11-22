var l = window.location;
var base_url = String.format("{0}//{1}/{2}", l.protocol, l.host, l.pathname.split('/')[1]);
var _path = String.format("{0}//{1}/", l.protocol, l.host);

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

$.url = function (url) {
    return _path + url;
}

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$(document).ajaxSend(function (event, xhr, settings) {
    if (!csrfSafeMethod(settings.type)) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
});

//$(function () {
//    $.ajaxSetup({
//        cache: false,
//        statusCode: { 401: function () { window.location = $.url("login/"); } },
//        beforeSend: function (xhr, settings) {
//            function getCookie(name) {
//                var cookieValue = null;
//                if (document.cookie && document.cookie != '') {
//                    var cookies = document.cookie.split(';');
//                    for (var i = 0; i < cookies.length; i++) {
//                        var cookie = jQuery.trim(cookies[i]);
//                        // Does this cookie string begin with the name we want?
//                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
//                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                            break;
//                        }
//                    }
//                }
//                return cookieValue;
//            }
//            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
//                // Only send the token to relative URLs i.e. locally.
//                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
//            }
//        }
//    });
//});