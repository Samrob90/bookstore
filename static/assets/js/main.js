$(document).ready(function () {
    const csftoken = Cookies.get('csrftoken');
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!(/^http:.*/.test(settings.url))) {
                xhr.setRequestHeader("X-CSRFToken", csftoken)
            }
        }
    })

    // Remove cart item from sidebare  
    $(".removeCartItem").click(function (e) {
        e.preventDefault();
        let this_ = $(this)
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
                        this_.closest(".sidebar_book_cart").fadeOut("slow");
                    }
                }
            },
            "json"
        );

    });
    // =================================================================================
    // suscribe to newsleter
    //================================================================================== 

    $(".suscribe_to_news_later").click(function (e) {
        e.preventDefault();
        const newletter_email = $(".suscribe_new_letter").val()
        // alert(newletter_email)
        if (newletter_email === "" || !validateEmail(newletter_email)) {
            $(".suscribe_new_letter").removeClass("border-dark").addClass("border-danger")
            $(".newsletter_error").removeClass("d-none")
        } else {
            $(".suscribe_new_letter").removeClass("border-danger").addClass("border-dark")
            $(".newsletter_error").addClass("d-none")

            const data_ = {
                "newsletter_suscription_email": newletter_email
            }
            $.post("/shopacc/", data_,
                function (data, textStatus, jqXHR) {
                    if (data.result === "failed") {
                        $(".newsletter_error").removeClass("d-none").html("It appears that you have already registered to receive our newsletter based on our records.")
                    } else if (data.result === "success") {
                        $("#newslettermodal").modal('show')
                        console.log("hello world")
                    }
                },
                "json"
            );



        }

    });

    // =================================================================================
    // seache for book title 
    //================================================================================== 
    $(".seache_book_by_title").focus(function (e) {
        e.preventDefault();
        $(".seache_book_by_title_result").fadeIn("slow")
        $(".seache_book_by_title").keypress(function (e) {
            // e.preventDefault()
            let input_value = $(this).val()
            let data = {
                "seache_from_seache_bar": input_value
            }
            $.post("/shopacc/", data,
                function (data, textStatus, jqXHR) {
                    if (data.url === null || data.title == null) {

                    } else {

                        $(".book_result_content").empty().html("<a href=' " + data.url + " '> " + data.title + " </a>")
                    }

                },
                "json"
            );
        });
    });

    $(".seache_book_by_title").focusout(function (e) {
        $(".seache_book_by_title_result").fadeOut()

    })






    function validateEmail($email) {
        var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
        return emailReg.test($email);
    }
});