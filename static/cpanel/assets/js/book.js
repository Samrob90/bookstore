$(document).ready(function () {
    const csftoken = Cookies.get('csrftoken');
    // const csftoken = $("input[name='csrfmiddlewaretoken']").val()
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!(/^http:.*/.test(settings.url))) {
                xhr.setRequestHeader("X-CSRFToken", csftoken)
            }
        }
    })
    let ImageUrl = ""
    // first step continue clicked
    $(".continue").click(function (e) {
        e.preventDefault();
        $(".preview").removeClass("d-none")
        $("#continue").addClass(" d-none")
        $(".first_").hide()

        $("#second").show()
        let files = $("#files")[0].files
        let data = new FormData($("#form").get(0))
        let title = $("#id_title").val()
        let author = $("#id_author").val()
        let quantity = $("#id_quantity").val()



        data.append("title", title)
        data.append("author", author)
        data.append("quantity", quantity)
        data.append("files", files)

        addDetails("Title :", title)
        addDetails("Author :", author)
        addDetails("Quantity :", quantity)
        readFile($("#files")[0].files[0])
        $("#outputimage").attr("src", ImageUrl)

        // add book type 
        let number = 0
        $(".addbooktype").click(function (e) {
            e.preventDefault();

            let booktype = $("#id_booktype").val()
            let booktypeprice = $("#id_booktypeprice").val()
            let booktypedescription = $("#description").val()

            let booktype_data = [booktype, booktypeprice, booktypedescription]
            // booktype_.push(booktype_data)
            // let name = "booktype_" + number

            data.append(booktype, booktype_data)

            if (booktypedescription != "" || booktypeprice != "") {
                addDetails(booktype, booktypeprice + " GHS")
                add_booktype_in_space(booktype, booktypeprice)
                $(".closemodal").click()
            }

            $("#id_booktype").val(" ")
            $("#id_booktypeprice").val(" ")
            $("#description").val(" ")
            number++

        });


        // previous click
        $(".previous").click(function (e) {
            e.preventDefault();
            $(".second").hide()
            $(".first_").show()
            $("#continue").removeClass(" d-none")
            $(".first_value_added").remove()
            $(".second_value_added").remove()
        });


        // next click
        $(".next").click(function (e) {
            e.preventDefault();
            // data.append("booktype", booktype_)

            $.ajax({
                url: "/cpanel/add-book",
                type: "POST",
                data: data,
                dataType: 'json',
                cache: false,
                processData: false,
                contentType: false,
                success: function (data, textStatus, jqXHR) {
                    if (data.result === "success") {
                        window.location.replace("/cpanel/add-book")
                    }
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    //if fails     
                }
            });
        });

    });



    function addDetails(title, value) {
        let html = "<li class='first_value_added'><strong> " + title + "</strong> <span>" + value + "</span></li>"
        $("#details_ul").append(html)
    }

    function add_booktype_in_space(booktype, booktypeprice) {
        let html_ = "<div class='alert alert-info second_value_added' role='alert'>" + booktype + " | " + booktypeprice + " GHS" + " </div>"
        $("#booktypecover").append(html_)
    }

    $("#files").change(function (e) {
        e.preventDefault();
        readFile($("#files")[0].files[0])

    });
    // previeew file

    function readFile(event) {
        var reader = new FileReader();
        reader.onload = function () {


            ImageUrl = reader.result


        };
        reader.readAsDataURL(event);
        // reader.readAsDataURL(event);

    };
});