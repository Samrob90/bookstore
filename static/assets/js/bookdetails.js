$(document).ready(function () {
    $(".ccs_child").hide()
    $(".preload-image-bookstrap").find(".preloader-newtonbookshop ").removeClass(" preloader-newtonbookshop ")
    $(".value_redirect").click(function (e) {
        e.preventDefault();
        const url = $(this).find("a").attr("href")
        window.location.href = url

    });



    const csftoken = Cookies.get('csrftoken');
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!(/^http:.*/.test(settings.url))) {
                xhr.setRequestHeader("X-CSRFToken", csftoken)
            }
        }
    })


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
    // detail page add to cart 
    // ================================================

    // $(".single_add_to_cart_button_detail_page").click(function (e) {
    //     e.preventDefault();
    //     let data = $("#details_product_form").serialize()
    //     alert(data)
    //     $(this).html("ADDING ..")

    //     $.ajax({
    //         type: "post",
    //         url: "/shopacc/",
    //         data: data,
    //         dataType: "json",
    //         success: function (response) {
    //             if (response.result === "success") {
    //                 location.reload()
    //             }
    //         }
    //     })

    // });

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
    $(".review_rating").click(function () {
        const star_one = $(".star_one").html()
        const star_two = $(".stars_two").html()
        const star_three = $(".star_three").html()
        const star_four = $(".star_four").html()
        const star_five = $(".stars_five").html()
        $(".star_one").closest("li").find(".progress-bar").attr("style", multiplyer(star_one))
        $(".star_two").closest("li").find(".progress-bar").attr("style", multiplyer(star_two))
        $(".star_three").closest("li").find(".progress-bar").attr("style", multiplyer(star_three))
        $(".star_four").closest("li").find(".progress-bar").attr("style", multiplyer(star_four))
        $(".star_five").closest("li").find(".progress-bar").attr("style", multiplyer(star_five))

    });

    function multiplyer(star, this_) {
        let percentage = Number(star) / Number(100)
        return "width:" + percentage + "%;"
    }

    // write a review

    $(".submit_review").click(function (e) {
        e.preventDefault();
        $(".loader").removeClass("d-none")
        $(this).css("opacity", "0.5")
        $("#loader_text").html("submiting..")

        $(".stars").click(function (e) {
            e.preventDefault()

        })
        const review_comment = $("#descriptionTextarea").val()

        $.post("url", data,
            function (data, ) {

            },
            "json"
        );
    });

});