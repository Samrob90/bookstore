$(document).ready(function () {
    const csftoken = Cookies.get('csrftoken');
    const url = "/checkout/"
    let addressid = 0,
        shippingcost = 0;
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!(/^http:.*/.test(settings.url))) {
                xhr.setRequestHeader("X-CSRFToken", csftoken)
            }
        }
    })
    // if user account section is displayed (if user is authenticated)
    if ($(".fetch_address").css("display") == "none") {

        // pass
    } else {
        // get selected user address id if address changed 
        $(".form-check input").click(function () {
            addressid = $(this).val()
            $(".select_address_error").addClass("d-none")
            shippinCost(addressid)
        })
        let TotalSum = Number($("#subtotal").attr("subtotal")) + Number($("#shipping_fee").html())
        $("#Total").html(TotalSum.toFixed(1))

    }

    // apply coupon
    $("#apply_coupon").click(function (e) {
        e.preventDefault();
        // get coupon value 
        const coupon = $("#coupon_code1").val()

        // check if address is filed or selected 
        let address = $(".fetch_address input[name='addressid']:checked").val()
        if (typeof address === "undefined") {
            // display error incase it was hidden 
            $(".select_address_error").removeClass("d-none")
            $("body").scrollTop(0); //scroll page back to top 
            $(".select_address_error").html("Please select address to preceed !")
        } else {
            let this_ = $(this)
            this_.css("opacity", "0.5")
            this_.val("proccessing..")
            if (coupon === "" || coupon.length === 0 || !coupon.replace(/\s/g, '').length) {
                $("#coupon_code1").css("border", "1px solid red")
                $("#coupon_error").html("Invalide input!")
                this_.css("opacity", "1")
                this_.val("Apply coupon")

            } else {
                const coupon_data = {
                    "coupon_code_check": 0,
                    "coupon": coupon,
                    "total": Number($("#Total").html())
                }
                $.post(url, coupon_data,
                    function (data) {
                        this_.css("opacity", "1")
                        this_.val("Apply coupon")
                        if (data.result === "valid") {
                            // let total = $("#Total").html()
                            $(".discount").addClass("d-none")
                            $(".applied_coupon").removeClass("d-none")
                            $("#discount__").html(data.discount)
                            $(".getdiscount").attr("discount", data.discount)
                            $("#Total").html(data.total.toFixed(1))

                        }

                    },
                    "json"
                ).fail(function (error) {
                    alert(error.responseJSON)
                });
            }
        }
    });

    function set_totals(shippincost) {
        let subtotal = $("#subtotal").attr("subtotal")
        let discount = $(".getdiscount").attr("discount")
        // alert(discount)
        let fees = shippincost
        let SubtotalSum = Number(subtotal) + Number(fees)
        if (Number(subtotal) >= 300) {
            fees = 0
        }
        if (discount !== "") {
            SubtotalSum = Number(SubtotalSum) - Number(discount)
        }

        $("#shipping_fee").html(fees.toFixed(1))
        $("#subtotal").html(SubtotalSum.toFixed(1))
        $("#Total").html(SubtotalSum.toFixed(1))

    }


    // calculate shippinCost 
    function shippinCost(addressid) {
        let data = {
            "addressid": addressid,
            "calculate_shipping_cost": 0
        }
        $.post(url, data,
            function (data, textStatus, jqXHR) {
                set_totals(shippingcost = data.result)
            },
            "Json"
        );
    }


    $("#pay_cash").click(function (e) {
        e.preventDefault()
        $("#pay_momo").find(".card-body").removeClass("select_payment_active")
        $(".selected_icone_pay_momo").addClass("d-none")
        $(this).find(".card-body").addClass("select_payment_active");
        $(".selected_icone_pay_cash").removeClass("d-none")
        $("#payment_method").attr("value", "pay_with_cash_on_delivery")
    })
    $("#pay_momo").click(function (e) {
        e.preventDefault();
        $("#pay_cash").find(".card-body").removeClass("select_payment_active")
        $(".selected_icone_pay_momo").removeClass("d-none")
        $(this).find(".card-body").addClass("select_payment_active");
        $(".selected_icone_pay_cash").addClass("d-none")
        $("#payment_method").attr("value", "pay_with_momo")

    });




});