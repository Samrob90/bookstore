$(document).ready(function () {

    const csftoken = Cookies.get('csrftoken');
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!(/^http:.*/.test(settings.url))) {
                xhr.setRequestHeader("X-CSRFToken", csftoken)
            }
        }
    })


    $(".shop_add_to_cart").click(function (e) {
        e.preventDefault();
        const parent_class = ".img-thumbnail-shop-newtonbookshop"
        const title = $(this).closest(parent_class).find("#booktitle").html()
        const type = $(this).closest(parent_class).find("#booktype").html()
        const img = $(this).closest(parent_class).find("img").attr("src")
        const price = $(this).attr("price")
        const product_id = $(this).attr("product_id")

        $(this).parent().find(".shop_add_to_cart_spinner").removeClass("d-none")

        $("#exampleModalCenter").modal("show")
        let this_ = $(this)



        let data = {
            'product_id': product_id,
            "shop_add_top_cart": "cart"
        }
        $.ajax({
            type: "post",
            url: "/shopacc/",
            data: data,
            dataType: "json",
            success: function (response) {
                this_.parent().find(".shop_add_to_cart_spinner").addClass("d-none")
                let img = "/media/thumbnail/" + response.result['bookthumbnail']
                $("#product_added_img").attr("src", img)
                $("#title").html(response.result['booktitle'])
                $("#bookprice_").html("Qty:" + response.result['bookquantity'] + "x " + "<span class='woocommerce-Price-currencySymbol'>GHS </span>" + response.result['bookprice'])
                $("#booktype_").html(response.result['booktype'])

            }
        });



    });


});