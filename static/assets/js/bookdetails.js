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

    // get avarage
    // const avg = Math.floor(Number($(".avarage_ratings").html()))
    // let stars = $(".average_review_icone").find(".stars_yellow")
    // stars.parent().nextAll().children('.fa-star').addClass("stars_yellow")

    // book review likes 
    $(".book_review_likes").click(function (e) {
        e.preventDefault();
        let l = $(this)
        const current_likes = l.find('span').html() //get current_likes value
        const bookid = l.find('span').attr("bookid") // get bookid 
        let types = false
        const commentid = l.attr("commentid")
        // check if user already liked the comment 
        if (l.find("i").hasClass("text-info")) {

        } else {
            l.find('span').html(Number(current_likes) + 1) //get current like and add 1 
            l.find("i").removeClass("text-dark").addClass("text-info") // change icone color to blue

            // send ajax request
            // check if user already disliked this comment ; By using  icone color
            if ($(".book_review_dislikes").find("i").hasClass("text-danger")) {
                //remove class text-danger and add text-dark 
                let dislikes = $(".book_review_dislikes")
                dislikes.find("i").removeClass("text-danger").addClass("text-dark")
                // update dislike total number by remove 1 on its current number
                dislikes.find("span").html(Number(dislikes.find("span").html()) - 1)
                dislikes = true
                // send ajax request
            }
            let data = {
                "review_likes": "likes",
                "bookid": bookid,
                "Other": types,
                "oposite": "dislikes",
                "commentid": commentid,
            }
            update_likes(data)
        }
    })



    // book review dislikes 
    $(".book_review_dislikes").click(function (e) {
        e.preventDefault();
        let d = $(this)
        const current_dislikes = d.find('span').html()
        const bookid = d.find('span').attr("bookid")

        // check if user has already disliked this comment
        if (d.find('i').hasClass('text-danger')) {
            // pass
        } else {
            d.find('span').html(Number(current_dislikes) + 1)
            d.find("i").removeClass("text-dark").addClass('text-danger')

            // send ajax request

            // check if user has already liked this comment 
            if ($(".book_review_likes").find('i').hasClass("text-info")) {
                let likes = $(".book_review_likes")
                likes.find("i").removeClass("text-info").addClass("text-dark")
                likes.find("span").html(Number(likes.find("span").html()) - 1)

                // send ajax request 
            }
        }
    })

    function update_likes(data) {
        $.post("/reviews/", data,
            function (data, textStatus, jqXHR) {

            },
            "json"
        );
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
                    }
                },
                "json"
            );
        }






    });


    // const star_one = $(".star_one").html()
    // const star_two = $(".stars_two").html()
    // const star_three = $(".star_three").html()
    // const star_four = $(".star_four").html()
    // const star_five = $(".stars_five").attr("id")
    // $(".star_one").closest("li").find(".progress-bar").attr("style", multiplyer(50))
    // $(".star_two").closest("li").find(".progress-bar").attr("style", multiplyer(star_two))
    // $(".star_three").closest("li").find(".progress-bar").attr("style", multiplyer(star_three))
    // $(".star_four").closest("li").find(".progress-bar").attr("style", multiplyer(star_four))
    // $(".star_five").closest("li").find(".progress-bar").attr("style", multiplyer(star_five))
    // alert(star_five)


    // write a review


});