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

                $("#svg").show()
                if (Number(response.result['bookquantity']) > 1) {
                    $("#bookprice_").html("Qty:" + response.result['bookquantity'] + " X " + "<span class='woocommerce-Price-currencySymbol'>GHS </span>" + response.result['bookprice'])
                } else {
                    $(".cart-contents-count").html(Number($(".cart-contents-count").html()) + 1)
                    $("#bookprice_").html("<span class='woocommerce-Price-currencySymbol'>GHS </span>" + response.result['bookprice'])
                }

                $("#exampleModalCenter").modal("show")
                $(".view__").html("View cart")
                $(".view__").attr("href", "/cart/")
                this_.parent().find(".shop_add_to_cart_spinner").addClass("d-none")
                let img = "/media/thumbnail/" + response.result['bookthumbnail']
                $(".action_added").html("Added to cart ")

                $("#product_added_img").attr("src", img)
                $("#title").html(response.result['booktitle'])

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
        $("#exampleModalCenter").modal("show")
        const product_id = $(this).attr("product_id")
        const data = {
            "product_id": product_id,
            "shop_add_top_cart": "wishlist"
        }
        let this_ = $(this)
        $.post(url, data,
            function (data, ) {


                $("#exampleModalCenter").modal("show")
                $(".view__").html("View wishlist")
                $(".view__").attr("href", "/account/wishlist/")


                if (data.result === "failed") {
                    $("#svg").hide()
                    let img = "/media/thumbnail/" + data.data['bookthumbnail']
                    $(".action_added").html("This item is already in your wishlist")
                    $("#product_added_img").attr("src", img)
                    $("#title").html(data.data['booktitle'])
                    $("#bookprice_").html("<span class='woocommerce-Price-currencySymbol'>GHS </span>" + data.data['bookprice'])
                    $("#booktype_").html(data.data['booktype'])
                } else if (data.result === "notauth") {
                    window.location.href = "/login"
                } else {
                    let img = "/media/thumbnail/" + data.data['bookthumbnail']
                    $(".action_added").html("Added to wishlist ")
                    $("#product_added_img").attr("src", img)
                    $("#title").html(data.data['booktitle'])
                    $("#bookprice_").html("<span class='woocommerce-Price-currencySymbol'>GHS </span>" + data.data['bookprice'])
                    $("#booktype_").html(data.data['booktype'])
                }

            },
            "json"
        );


    });



    // filter by
    const FILTER_URL = $(location).attr('href')
    let FILET_URL_SET = "/shop/?q="
    $(".filter_by_side_body .product-categories a").click(function (e) {
        e.preventDefault();
        let value = $(this).html()
        if ($(this).closest("div").hasClass("product-categories")) {

        }
    });




});