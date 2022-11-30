$(document).ready(function () {
    const url = "/shopacc/"
    const csftoken = Cookies.get('csrftoken');
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!(/^http:.*/.test(settings.url))) {
                xhr.setRequestHeader("X-CSRFToken", csftoken)
            }
        }
    })

    // ============================================================================
    // shop add to cart 
    //============================================================================== 
    $(".shop_add_to_cart").click(function (e) {
        e.preventDefault();
        $(this).parent().find(".shop_add_to_cart_spinner").removeClass("d-none")

        let this_ = $(this)
        const product_id = $(this).attr("product_id")
        let data = {
            'product_id': product_id,
            "shop_add_top_cart": "cart"
        }
        $.ajax({
            type: "post",
            url: url,
            data: data,
            dataType: "json",
            success: function (response) {
                $("#exampleModalCenter").modal("show")
                this_.parent().find(".shop_add_to_cart_spinner").addClass("d-none")
                let img = "/media/thumbnail/" + response.result['bookthumbnail']
                $(".action_added").html("Added to cart ")
                $("#product_added_img").attr("src", img)
                $("#title").html(response.result['booktitle'])
                $("#bookprice_").html("Qty:" + response.result['bookquantity'] + "x " + "<span class='woocommerce-Price-currencySymbol'>GHS </span>" + response.result['bookprice'])
                $("#booktype_").html(response.result['booktype'])

            }
        });



    });


    // ============================================================================
    // shop add to wishlist
    //============================================================================== 
    $(".shop_add_to_wishlist").click(function (e) {
        e.preventDefault();
        // alert("hwlwlo")
        // $("#exampleModalCenter").modal("show")
        const product_id = $(this).attr("product_id")
        const data = {
            "product_id": product_id,
            "shop_add_top_cart": "wishlist"
        }
        $(".account_side_bar").click();
        let this_ = $(this)
        $.post(url, data,
            function (data, ) {
                $("#exampleModalCenter").modal("show")
                if (data.result === "failed") {

                } else if (data.result === "notauth") {

                } else {

                    let img = "/media/thumbnail/" + response.result['bookthumbnail']
                    $(".action_added").html("Added to cart ")
                    $("#product_added_img").attr("src", img)
                    $("#title").html(response.result['booktitle'])
                    $("#bookprice_").html("<span class='woocommerce-Price-currencySymbol'>GHS </span>" + response.result['bookprice'])
                    $("#booktype_").html(response.result['booktype'])
                }

            },
            "json"
        );


    });


});