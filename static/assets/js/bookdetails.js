$(document).ready(function () {
    $(".ccs_child").hide()
    $(".preload-image-bookstrap").find(".preloader-newtonbookshop ").removeClass(" preloader-newtonbookshop ")
    $(".value_redirect").click(function (e) {
        e.preventDefault();
        const url = $(this).find("a").attr("href")
        window.location.href = url

    });



    // const csftoken = Cookies.get('csrftoken');
    // $.ajaxSetup({
    //     beforeSend: function (xhr, settings) {
    //         if (!(/^http:.*/.test(settings.url))) {
    //             xhr.setRequestHeader("X-CSRFToken", csftoken)
    //         }
    //     }
    // })


    // ================================================
    // quantity js minute 
    // ================================================

    // minus
    $(".js-minus").click(function (e) {
        e.preventDefault()
        let input_value = $(".js-result").val()
        if ((Number(input_value)) > 1) {
            let newValue = Number(input_value) - 1
            $(".js-result").val(newValue)
        }
    })

    // plus
    $(".js-plus").click(function (e) {
        e.preventDefault()
        let input_value = $(".js-result").val()
        if (Number(input_value) >= 0) {
            $(".js-result").val(Number(input_value) + 1)
        }
    })

    // =================================================
    // Remove cart items
    // ================================================

    $(".removeCartItem").click(function (e) {
        e.preventDefault();
        const product_id = $(this).attr("id")
        const booktype = $(this).attr("booktype")
        const pathname = window.location.pathname

        const data = {
            "removeCartItem": true,
            "product_id": product_id,
            "booktype": booktype
        }
        $.post("/shopacc/", data,
            function (data, textStatus, jqXHR) {
                if (data.result === "success") {
                    if (pathname === "/cart/") {

                        location.reload()
                    } else {

                    }
                }
            },
            "json"
        );

    });

    // =================================================
    // Add to wish list
    // ================================================
    $(".add_to_wish_list").click(function (e) {
        e.preventDefault();
        const bookid = $(this).attr("bookid")
        let data = {
            "add_to_wishlist_bookdetails_page": "wishlist",
            "bookid": bookid
        }
        $.post("/shopacc/", data,
            function (data, ) {
                location.reload()
                // print(data.result)
            },
            "json"
        );
    });


    // rating
    $(".startfunc").click(function () {

        let star = $(this)

        $(".startfunc").removeClass("stars_yellow").removeClass("stars_gray")
        // make current start yellow
        star.removeClass("stars_gray").addClass("stars_yellow")
        // make previouse star yellow 
        star.parent().prevAll().children('.startfunc').addClass("stars_gray")
        // make next star gray 
        star.parent().nextAll().children('.startfunc').addClass("stars_yellow")

        $(".rating").attr("value", star.attr("title"))

        // set attr titlet ot input field 


    });


    function multiplyer(star, this_) {
        let percentage = Number(star) / Number(100)
        return "width:" + percentage + "%;"
    }



    $(".submit_review").click(function (e) {
        e.preventDefault();
        $(".loader").removeClass("d-none")
        $(this).css("opacity", "0.5")
        $("#loader_text").html("submiting..")
        const rating = $(".rating").val()
        const review_comment = $("#descriptionTextarea").val()
        const title = $("#review_title").val()
        if (rating === "") {
            $("#rating_error").removeClass("d-none")
            $(".loader").addClass("d-none")
            $(this).css("opacity", "1")
            $("#loader_text").html("Submit Review")
        } else if (title == "") {
            $("#rating_error").removeClass("d-none")
            $(".loader").addClass("d-none")
            $(this).css("opacity", "1")
            $("#loader_text").html("Submit Review")
            $("#rating_error").html("Title field can not be empty")
            $("#review_title").css("border", "1px solid red")
        } else {
            let data = {
                "book_review": "true",
                "rating": rating,
                "commet": review_comment,
                "bookid": $("#bookid").val(),
                "review_title": title
            }

            $.post("/reviews/", data,
                function (data, ) {
                    $("#rating_error").removeClass("d-none")
                    $(".loader").addClass("d-none")
                    $(".submit_review").css("opacity", "1")
                    $("#loader_text").html("Submit Review")
                    if (data.status === "success") {
                        $("#rating_error").removeClass("d-none").removeClass("alert alert-danger").addClass("alert alert-success")
                        $("#rating_error").html("Comment Successfully submited")
                        $("#descriptionTextarea").val("")
                        $("#review_title").val("")
                    }
                },
                "json"
            );
        }
    });

    // write a review

    $(".share").hover(function () {
        // over
        $(".share_social_media").toggle();

    }, function () {
        // out
        // $(".share_social_media").fadeOut();
    });
    $(".share_social_media").mouseleave(function () {
        $(this).fadeOut();
    });


    // reset selected element 
    // alert($(".book_format_on_change option:selected").val())
    // $(".book_format_on_change option:selected").prop('selected', true);
    // $(".book_format_on_change option:selected").attr("value", $(".default_book_price").attr("default_book_type"))
    // // Book type price on change 
    // $(".book_format_on_change").change(function (e) {
    //     // alert("hello world")
    //     const booktype = $(this).val().split(" ")
    //     let booktypename = booktype[0]
    //     let booktypeprice = booktype[1]
    //     let default_bookprice = $(".default_book_price").val()
    //     let default_booktype = $(".default_book_price").attr("default_book_type")
    //     let has_discount = $(".default_book_price").attr("has-discount")

    //     if (has_discount === "false") {
    //         $(".default_book_price").html(booktypeprice)
    //     } else {

    //     }

    // });

});