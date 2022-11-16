$(document).ready(function () {
    let ImageUrl = ""
    $(".continue").click(function (e) {
        e.preventDefault();
        $(".preview").removeClass("d-none")
        $("#continue").addClass(" d-none")
        $(".first_").hide()

        $("#second").show()

        let data = new FormData()
        let title = $("#id_title").val()
        let author = $("#id_author").val()
        let quantity = $("#id_quantity").val()



        data.append("title", title)
        data.append("author", author)
        data.append("quantity", quantity)

        addDetails("Title :", title)
        addDetails("Author :", author)
        addDetails("Quantity :", quantity)
        $("#outputimage").attr("src", ImageUrl)


        $(".addbooktype").click(function (e) {
            e.preventDefault();
            let booktype = $("#id_booktype").val()
            let booktypeprice = $("#id_booktypeprice").val()
            let booktypedescription = $("#description").val()

            data.append("booktype", booktype)
            data.append("booktype_price", booktypeprice)
            data.append("booktype_description", booktypedescription)


            if (booktypedescription != "" || booktypeprice != "") {
                addDetails(booktype, booktypeprice + " GHS")
                add_booktype_in_space(booktype, booktypeprice)
                $(".closemodal").click()
            }

            $("#id_booktype").val(" ")
            $("#id_booktypeprice").val(" ")
            $("#description").val(" ")

        });

    });



    function addDetails(title, value) {
        let html = "<li><strong> " + title + "</strong> <span>" + value + "</span></li>"
        $("#details_ul").append(html)

    }

    function add_booktype_in_space(booktype, booktypeprice) {
        let html_ = "<div class='alert alert-info' role='alert'>" + booktype + " | " + booktypeprice + " GHS" + " </div>"
        $("#booktypecover").append(html_)
    }

    $("#files").change(function (e) {
        e.preventDefault();
        readFile(e)

    });
    // previeew file

    function readFile(event) {
        var reader = new FileReader();
        reader.onload = function () {


            ImageUrl = reader.result

        };
        reader.readAsDataURL(event.target.files[0]);
    };
});