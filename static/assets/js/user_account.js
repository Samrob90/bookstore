$(document).ready(function () {
    //  ===================================================================
    // EDIT USER ADDRESSS -account
    // =====================================================================
    $(".edit_user_address").click(function (e) {
        e.preventDefault();
        let first_name = $(this).attr("first_name"),
            last_name = $(this).attr("last_name"),
            city = $(this).attr("city"),
            region = $(this).attr("region"),
            country = $(this).attr("country"),
            phonenumber = $(this).attr("phonenumber"),
            address1 = $(this).attr("address1"),
            address2 = $(this).attr("address2"),
            addressid = $(this).attr("addressid");

        $(".addresspk").val(addressid)
        $(".user_edit_address_form").find("input[name='billing_first_name'],input[name='billing_last_name'],input[name='billing_city'],select[name='billing_country'],input[name='billing_state'],input[name='billing_phone'],input[name='billing_address_1']").attr("required", "required")

        $(".user_edit_address_form").find("input").css("color", "black")
        $(".user_edit_address_form").find("input[name='billing_first_name']").val(first_name)
        $(".user_edit_address_form").find("input[name='billing_last_name']").val(last_name)
        $(".user_edit_address_form").find("input[name='billing_city']").val(city)
        $(".user_edit_address_form").find("select[name='billing_country']").val(country).prop("selected", true)
        $(".user_edit_address_form").find("input[name='billing_state']").val(region)
        $(".user_edit_address_form").find("input[name='billing_phone']").val(phonenumber)
        $(".user_edit_address_form").find("input[name='billing_address_1']").val(address1)
        $(".user_edit_address_form").find("input[name='billing_address_2']").val(address2)


    });
});