$(document).ready(function () {

    $(".qtyupdate").click(function (e) {
        e.preventDefault()
        let qty = 0
        let NewQtx = $(this).parent("div").find("input[type='number']").val()
        let bookid = $(this).parent("div").find("input[type='number']").attr("bookid")
        if ($(this).hasClass("js-minus")) {
            if (Number(NewQtx) > 1) {
                qty = Number(NewQtx) - 1
                $(this).parent("div").find("input[type='number']").val(qty)
            }
        } else {
            qty = Number(NewQtx) + 1
            $(this).parent("div").find("input[type='number']").val(qty)
        }
        const data = {
            "cart_update_qty": qty,
            "bookid": bookid
        }
        update_cart(data, "inc")
    })

    $(".cart_update_keypress").keypress(function (e) {
        // e.preventDefault()
        if (e.which == 13) {
            let quantity = $(this).val()
            let book_id = $(this).attr("bookid")
            let keydow_data = {
                "cart_update_qty": quantity,
                "bookid": book_id,
                "keypress": "key"
            }
            update_cart(keydow_data, "keypress")
        }
    });


    // ajax function to update on server side 
    function update_cart(data, type) {
        $.ajax({
            type: "POST",
            url: "/shopacc/",
            data: data,
            dataType: "json",
            success: function (response) {
                if (response.result === "success") {
                    if (type === "keypress") {
                        location.reload()
                    }
                }
            }
        });
    }
});