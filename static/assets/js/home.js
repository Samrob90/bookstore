$(document).ready(function () {
    $(".js-slide").removeClass("d-none")

    // book loader fade out 
    $(".bookloader_").hide()
    $(".bookloaded_").removeClass("d-none")


    if ($(".dealoftheweek").css("display") === "none") {

    } else {
        let stamp = $(this)
        let timestamp = stamp.find(".time_hold")
        // // console.log(timestamp)
        // console.log(timestamp.length)
        // for (let times in timestamp) {
        //     console.log(timestamp[times])
        //     // console.log(times.attr("offerends"))
        // }

        for (let i = 0; i < timestamp.length; i++) {
            let timestamp_value = timestamp[i].attributes['offerends'].value
            stamp.find(".days").html(1)


            // setInterval(function () {
            //     makeTimer(timestamp_value);
            // }, 1000);
            // console.log(timestamp[i]['attr'])
        }
    }


    // timer

    function makeTimer(timestamp) {
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

        $(".days").html(days);
        $(".hours").html(hours);
        $(".minutes").html(minutes);
        $(".seconds").html(seconds);

    }



});