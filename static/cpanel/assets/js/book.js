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

    $(".search_bar").keydown(function (e) {
        if (e.keyCode == 13) {
            e.preventDefault()
            const seache_bar_title = $(this).val()
            const data = {
                "title": seache_bar_title,
                "book_seach": "on"
            }
            $(".loader__").removeClass("d-none")
            $(".bookfind_seacher").addClass("d-none")
            $.post("/cpanel/bookfinder/", data,
                function (data, textStatus, jqXHR) {
                    $(".loader__").addClass("d-none")
                    if (data.data === null) {
                        $(".bookfind_seacher").removeClass("d-none")
                        $(".bookfind_seacher").empty().html("<h4 class='text-center text-muted'>No result found for your search.</h4>")
                    } else {
                        const paperback = data.data[0]
                        const bookinfo = data.data[1]
                        const ebook = data.data[2]
                        $(".bookfind_seacher").removeClass("d-none")
                        // $(".bookfind_seacher").empty()
                        $("#search_images").attr("src", bookinfo.book_thumbnail)
                        $("#search_author").html(bookinfo.author)
                        $("#searc_title").html(bookinfo.title)
                        $("#seach_description").html(bookinfo.description)
                        $(".search_book_details").empty()
                        for (let s in paperback) {
                            $(".search_book_details").append("<li><stron>" + s + "</strong> :" + paperback[s] + "</li>")

                        }
                        $(".search_ebook_details").empty()
                        for (let a in ebook) {
                            $(".search_ebook_details").append("<li><stron>" + a + "</strong> :" + ebook[a] + "</li>")
                        }


                        // ===================================================================================
                        // saved online book 
                        // ===================================================================================
                        $(".save_searched_book").click(function (e) {
                            e.preventDefault();
                            $('#defaultCheck12').prop('checked', false); // Unchecks it
                            $('#defaultCheck11').prop('checked', false); // Unchecks it
                            $('#defaultCheck10').prop('checked', true); // check it
                            // Paperback 
                            $("#defaultCheck10").click(function (e) {
                                if ($(this).is(':checked')) {
                                    $(".paperback").removeClass("d-none")
                                } else {
                                    if (!$(".paperback").hasClass("d-none")) {
                                        $(".paperback").addClass("d-none")
                                    }
                                }

                            });
                            //    AUDIOBOOK
                            $("#defaultCheck12").click(function (e) {
                                if ($(this).is(':checked')) {
                                    $(".audiobook").removeClass("d-none")
                                } else {
                                    if (!$(".audiobook").hasClass("d-none")) {
                                        $(".audiobook").addClass("d-none")

                                    }
                                }

                            });

                            // ebook
                            $("#defaultCheck11").click(function (e) {
                                if ($(this).is(':checked')) {
                                    $(".ebook").removeClass("d-none")
                                } else {
                                    if (!$(".ebook").hasClass("d-none")) {
                                        $(".ebook").addClass("d-none")

                                    }
                                }

                            });
                            // save book to database
                            $(".save_seache_book_google").click(function (e) {
                                e.preventDefault();
                                $(".save_seache_book_google").css("opacity", "0.5")
                                $(".save_seache_book_google").html("processing...")


                                if ($("#defaultCheck10").is(":checked") && $("#paperbackprice").val() == "") {
                                    seacher_error("Paperback price field is required !", "show")
                                } else if ($("#defaultCheck12").is(":checked") && $("#audibook_price").val() == "") {
                                    seacher_error("Audiobook price field can't be empty !", "show")
                                } else if ($("#defaultCheck11").is(":checked") && $("#ebook_price").val() == "") {
                                    seacher_error("ebook price field can't be empty !", "show")
                                } else if ($(".category").val() == "Open this select menu") {
                                    seacher_error("category field can't be empty !", "show")

                                } else {

                                    const form_val = $("#search_form").serializeArray()

                                    const formData = {
                                        "form_val": JSON.stringify(form_val),
                                        "bookinfo": JSON.stringify(bookinfo),
                                        "paperbook": JSON.stringify(paperback),
                                        "ebook": JSON.stringify(ebook)
                                    }

                                    $.post("/cpanel/bookfinder/", formData,
                                        function (data, textStatus, jqXHR) {
                                            seacher_error("", "hide")
                                        },
                                        "json"
                                    );


                                }

                            });


                        });
                    }

                },
                "json"
            );
        }
    });


    function seacher_error(message, type = "hide") {
        if (type === "show") {
            $(".book_seach_add_error").removeClass("d-none")
            $(".book_seach_add_error").html(message)
            $(".save_seache_book_google").css("opacity", "1")
            $(".save_seache_book_google").html("add")
        } else {
            $(".save_seache_book_google").css("opacity", "1")
            $(".save_seache_book_google").html("add")
            $(".book_seach_add_error").empty()
            $(".book_seach_add_error").addClass("d-none")

        }
    }
});