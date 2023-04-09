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
});