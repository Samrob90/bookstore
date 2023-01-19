$(document).ready(function () {
    // fecth notification user 
    const csftoken = Cookies.get('csrftoken');
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!(/^http:.*/.test(settings.url))) {
                xhr.setRequestHeader("X-CSRFToken", csftoken)
            }
        }
    })
    const data = {
        "cpanel_get_notification": "Notification"
    }
    $.post("/cpanel/get_notification/", data,
        function (data, textStatus, jqXHR) {
            $(".new_order").html(data.new_order)
            $(".in_progress").html(data.in_progress)
        },
        "json"
    );
});