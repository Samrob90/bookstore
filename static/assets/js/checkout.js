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
        alert("hello world")
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
        if (typeof address === "undefined" && $(".add_address_section").css("display") === "none") {
            // display error incase it was hidden 
            $(".select_address_error").removeClass("d-none")
            $("body").scrollTop(0); //scroll page back to top 
            $(".select_address_error").html("Please select address to proceed !")
        } else if (typeof address === "undefined" && $("#billing_country").val() === "") {
            $(".country_error").removeClass("d-none")
            $(".country_error").html("Please select country")
        } else {
            let this_ = $(this)
            coupon_show_load("show")

            if (coupon === "" || coupon.length === 0 || !coupon.replace(/\s/g, '').length) {
                $("#coupon_code1").css("border", "1px solid red")
                $("#coupon_error").html("Invalide input!")
                coupon_show_load("hide")
                $("#c_loader_text").val("Apply coupon")

            } else {
                const coupon_data = {
                    "coupon_code_check": 0,
                    "coupon": coupon,
                    "total": Number($("#Total").html())
                }
                $.post(url, coupon_data,
                    function (data) {
                        coupon_show_load("hide")
                        if (data.result === "valid") {
                            // let total = $("#Total").html()
                            $(".discount").addClass("d-none")
                            $(".applied_coupon").removeClass("d-none")
                            $("#discount__").html(data.discount)
                            $(".getdiscount").attr("discount", data.percentage)
                            $("#Total").html(data.total.toFixed(1))
                            $("#coupon_code_input").attr("value", coupon)
                        } else {
                            $("#coupon_code1").css("border", "1px solid red")
                            $("#coupon_error").html("coupon code is Invalide or expired !")
                        }
                    },
                    "json"
                ).fail(function (error) {
                    alert(error.responseJSON)
                });
            }
        }
    });



    // add new new shipping address
    $(".new_address").click(function (e) {
        e.preventDefault();
        $(".select_address_section").hide()
        $(".new_address").addClass("d-none")
        $(".select_user_address").removeClass("d-none")
        $(".add_address_section").removeClass("d-none")
        $(".fetch_address input[name='addressid']:checked").removeAttr("checked")
    });

    // switch back to select address
    $(".select_user_address").click(function (e) {
        e.preventDefault();
        $(".select_address_section").show() // dislay user address
        $(".new_address").removeClass("d-none") // show button to add new address
        $(".select_user_address").addClass("d-none") // hide button add new address 
        $(".add_address_section").addClass("d-none") // hide new address form
        $("#billing_country").val(" ") // set address country val to empty 

    });


    // if country value changes
    $("#billing_country").change(function (e) {
        e.preventDefault();
        $(".country_error").addClass("d-none") // hide country error 
        const country = $(this).val() // get country value to calculate shipping fee
        const city = $("#billing_city").val() // get city value to calculate shipping fee
        let shippingFee = 0 // declare empty shipping fee
        // check if country and cirty are not empty 
        if (country !== "") {

            if (country === "Ghana") {
                if (city === "") {
                    // delivery fee for Ghana varies in two diffente cities
                    // if user click apply button before filling city field
                    // show error 
                    // then when user filled city input get value and process shipping cost 
                    $(".city_error").removeClass("d-none")
                    $(".city_error").html("This field can't be empty")
                    $("#billing_city").focusout(function (e) {
                        shippingFee = delivery_fee_in_ghana($(this).val())
                        $(".city_error").addClass("d-none")
                        // ?
                        set_totals(shippingFee, country)
                    });
                } else {
                    shippingFee = delivery_fee_in_ghana(city)
                }

            } else {
                shippingFee = 455
            }

            set_totals(shippingFee)
        }




    });



    // proceed to next step 
    $(".proceed_to_next_step").click(function (e) {
        e.preventDefault();
        // check if user address is not empty or(if user is authenticated )
        let addressid = $(".fetch_address input[name='addressid']:checked").val()
        let THIS = $(this)
        continue_step_loader("show")
        if (typeof addressid === "undefined" && $(".add_address_section").css("display") === "none") {
            continue_step_loader("hide")
            $("body").scrollTop(0); //scroll page back to top 
            $(".select_address_error").removeClass("d-none")
            $(".select_address_error").html("Please select address to proceed !")
        } else if ($(".add_address_section").css("display") !== "none") {
            const first_name = $("#billing_first_name").val()
            const last_name = $("#billing_last_name").val()
            const country = $("#billing_country").val()
            const address1 = $("#billing_address_1").val()
            const city = $("#billing_city").val()
            const region = $("#billing_state").val()
            const phone_number = $("#billing_phone").val()
            const email = $("#billing_email").val()


            if (valide_billing_value(first_name, ".first_name_error") === false || valide_billing_value(last_name, ".last_name_error") === false || valide_billing_value(country, ".country_error") === false || valide_billing_value(address1, ".address1_error") === false || valide_billing_value(city, ".city_error") === false || valide_billing_value(region, ".region_error") === false || valide_billing_value(phone_number, ".phone_error") === false) {
                continue_step_loader("hide")

            } else if ($(".email_field").css("display") != "none" && valide_billing_value(email, ".email_error") === false) {
                alert("email is not none")
                continue_step_loader("hide")
            } else {
                proccess()

            }


        } else {
            proccess()
        }
    });

    function proccess() {
        const data = $("#checkout_form").serialize()
        // alert(data)
        $.post(url, data,
            function (data, textStatus, xhr) {
                if (data.result === "success" && data.type === "COD") {
                    window.location.replace("/order/success/" + data.orderNumber + "/")
                    continue_step_loader("hide")
                } else if (data.result === "success" && data.type === "PO") {
                    continue_step_loader("hide")
                    payWithPaystack(data.obj)

                }
            },
            "json"
        ).fail(function () {
            // continue_step_loader("hide")
            $(".proccess_error").removeClass("d-none")
            window.scrollTo(0, 0);
            $(".proccess_error").html("<strong> Somthing went wrong !!</strong> Try again in few minutes. If this persist, Please contact support to place your order manually  <strong>info@Newtonbookshop.com</strong>")

        })
    }


    function valide_billing_value(value, errorid) {
        state = false
        if (value === "" || value.length === 0 || !value.replace(/\s/g, '').length) {
            $(errorid).removeClass("d-none")
            $(errorid).html("Field required")
            $(errorid).closest("p").find("input").css("border", "1px solid red")
            window.scrollTo(0, 0);

        } else {
            $(errorid).hide()
            $(errorid).closest("p").find("input").css("border", "1px solid lightgray")

            state = true
        }
        return state
    }

    // chowcoupon togglw
    $(".showcoupon").click(function (e) {
        e.preventDefault();
        $(".coupon_toggle").toggle();
    });





    function delivery_fee_in_ghana(city) {
        if (city.toLowerCase() === "tema") {
            fees = 50
        } else if (city.toLowerCase() === "accra") {
            fees = 35
        } else {
            fees = 60
        }
        return fees
    }


    function set_totals(shippincost, country) {
        console.log(shippincost)
        let subtotal = $("#subtotal").attr("subtotal")
        let percentage = $(".getdiscount").attr("discount")
        // alert(discount)
        let fees = shippincost
        if (Number(subtotal) >= 300 && country === "Ghana") {
            fees = 0
        }

        let SubtotalSum = Number(subtotal) + Number(fees)
        let total = SubtotalSum
        if (percentage !== "") {
            let discount = (Number(SubtotalSum) * Number(percentage)) / 100
            total = Number(SubtotalSum) - Number(discount)
            $("#discount__").html(discount)
        }

        $("#shipping_fee").html(fees.toFixed(1))
        $("#subtotal").html(SubtotalSum.toFixed(1))
        $("#Total").html(total.toFixed(1))

    }


    function coupon_show_load(type) {
        if (type === "show") {
            $("#c_loader_text").css("opacity", "0.5")
            $("#c_loader_text").val("processing..")
            $(".c_loader").show()
        } else {
            $("#c_loader_text").css("opacity", "1")
            $("#c_loader_text").val("Apply coupon")
            $(".c_loader").hide()

        }
    }

    function continue_step_loader(type) {
        if (type === "show") {
            $(".processing").show()
        } else {
            $(".processing").hide()
        }
    }

    // calculate shippinCost 
    function shippinCost(addressid) {
        let data = {
            "addressid": addressid,
            "calculate_shipping_cost": 0
        }
        $.post(url, data,
            function (data, textStatus, jqXHR) {
                set_totals(data.result)
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






    // ===================================================
    // checkout
    // ===================================================


    // const paymentForm = document.getElementById('paymentForm');

    // paymentForm.addEventListener("submit", payWithPaystack, false);

    function payWithPaystack(data) {
        let handler = PaystackPop.setup({

            key: data.pk,

            email: data.email,

            amount: Number(data.amount) * 100,

            ref: data.reference,

            currency: "GHS",


            onClose: function () {

                window.location = `/complete_payment/${data.reference}/?np=cls`
            },

            callback: function (response) {
                console.log(response)
                window.location = `/complete_payment/${response.reference}/`
            }

        });



        handler.openIframe();

    }


});