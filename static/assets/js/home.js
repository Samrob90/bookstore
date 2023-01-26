$(document).ready(function () {
    $(".js-slide").removeClass("d-none")

    // book loader fade out 
    $(".bookloader_").hide()
    $(".bookloaded_").removeClass("d-none")




    let interval = setInterval(() => {
        check()
    }, 1000);

    function check() {
        if ($(".dealoftheweek").css("display") === "none") {
            clearInterval(interval)
        } else {
            $(".dealofweek_book").each(function (e) {
                let stamp = $(this)
                let timestamp_value = stamp.find(".time_hold").attr("offerends")
                makeTimer(timestamp_value, stamp)
            })
        }
    }


    // timer

    function makeTimer(timestamp, stamp) {
        var endTime = new Date(timestamp * 1000);
        endTime = (Date.parse(endTime) / 1000);

        var now = new Date();
        now = (Date.parse(now) / 1000);

        var timeLeft = endTime - now;

        var days = Math.floor(timeLeft / 86400);
        var hours = Math.floor((timeLeft - (days * 86400)) / 3600);
        var minutes = Math.floor((timeLeft - (days * 86400) - (hours * 3600)) / 60);
        var seconds = Math.floor((timeLeft - (days * 86400) - (hours * 3600) - (minutes * 60)));

        if (hours < "10") {
            hours = "0" + hours;
        }
        if (minutes < "10") {
            minutes = "0" + minutes;
        }
        if (seconds < "10") {
            seconds = "0" + seconds;
        }

        stamp.find(".days").html(days);
        stamp.find(".hours").html(hours);
        stamp.find(".minutes").html(minutes);
        stamp.find(".seconds").html(seconds);

    }



});