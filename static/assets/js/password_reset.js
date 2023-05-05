$(document).ready(function () {
    // password reset confirm
    const classVal = "form-control rounded-0 height-4 px-4"
    let password1 = $("#id_new_password1")
    password1.addClass(classVal)
    password1.attr("placeholder", "Enter new password")

    let password2 = $("#id_new_password2")
    password2.addClass(classVal)
    password2.attr("placeholder", "Confirm new password")

});