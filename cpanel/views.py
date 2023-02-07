from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from . import form
from django.contrib.auth import authenticate, login, logout
from authentications.models import Account
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from . import models
from PIL import Image
from frontend.models import category

# from random import Random, random
from bookstore.settings import BASE_DIR
import uuid, os
from django.template.defaultfilters import slugify
from .bookfinder.bookfinder import search_books
import requests
import tempfile
from django.core import files
from io import BytesIO
import json

# Create your views here.

# cpanel login
class CpanelLoginView(TemplateView):
    template_name = "cpanel/accounts/login.html"
    class_form = form.LoginForm

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name, {"form": self.class_form})

    def post(self, request, *args, **kwargs):
        form = self.class_form(request.POST)
        if form.is_valid():
            """
            .To authenticate user with username
            .first we check if username exist then get email of username
            .then authenticate user with the email
            """
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            # print(Account.objects.get(username))

            email = Account.objects.filter(username=username).first()
            if email is not None:
                user = authenticate(request, email=email.email, password=password)
                if user:
                    if user.is_staff or user.is_superuser or user.is_admin:
                        login(request, user)
                        return redirect("cpanel_dashboard")
                    else:
                        messages.error(
                            request,
                            "You do not have permition to access this page. ",
                        )
                else:
                    messages.error(request, "Incorrect username or password.")
            else:
                messages.error(request, "Incorrect username or password")

        else:
            messages.error(request, "Incorrect username or password.")

        return render(request, self.template_name, {"form": form})


class CpanelDashboardView(TemplateView):
    template_name = "cpanel/home/content/dashboard.html"


class CpanelBooksView(ListView):
    template_name = "cpanel/home/content/book.html"
    model = models.book
    paginate_by = 20
    context_object_name = "books"

    def post(self, request, *args, **kwargs):
        if "delete_book" in request.POST:
            bookpk = request.POST.get("bookid")
            # delete book
            try:
                models.book.objects.filter(pk=bookpk).delete()
                messages.success(request, "Book deleted successfuly")
            except Exception as e:
                messages.error(request, "Error : {e}")

            return redirect("cpanel_books")


class CpanelBookEdit(DetailView):
    model = models.book
    template_name = "cpanel/home/content/bookview.html"
    context_object_name = "book"


class OrdersViews(ListView):
    template_name = "cpanel/home/content/new_orders.html"
    model = models.order
    context_object_name = "new_orders"
    paginate_by = 20

    def get_queryset(self):
        return self.model.objects.filter(status="pending").order_by("-created_at")


class NewOrderDetails(DetailView):
    model = models.order
    template_name = "cpanel/home/content/new_order_details.html"
    context_object_name = "order_detail"

    def post(self, request, *args, **kwargs):
        order_id = request.POST.get("orderid")
        if "confirm_order" in request.POST:
            # confirm order
            self.change_order_status(
                order_id,
                "confirmed",
                "Order condirmed successfully",
            )
            return redirect("order_in_progress")

        if "cancel_order" in request.POST:
            self.change_order_status(
                order_id, "canceled", "Order canceled successfully"
            )
            return redirect("cpanel_completed_order")

        if "complete_order" in request.POST:
            message = "Order status changed successfully"
            self.change_order_status(order_id, "delivered", message)
            return redirect("cpanel_completed_order")

    def change_order_status(self, order_id, status, message):
        models.order.objects.filter(orderid=order_id).update(status=status)
        messages.success(self.request, message)

        # send email to update user of order status
        # send this to task


class CompletedOrder(ListView):
    model = models.order
    template_name = "cpanel/home/content/order_completed.html"
    context_object_name = "cpanel_order_completed"
    paginate_by = 20

    def get_queryset(self):
        unwamted_fields = ["pending", "confirmed"]
        return self.model.objects.exclude(
            status__in=[o for o in unwamted_fields]
        ).order_by("-created_at")


class OrderInProgress(ListView):
    model = models.order
    template_name = "cpanel/home/content/order_in_process.html"
    context_object_name = "order_in_progress"
    paginate_by = 20

    def get_queryset(self):
        unwamted_fields = ["pending", "complete", "delivered", "canceled"]
        return self.model.objects.exclude(status__in=[o for o in unwamted_fields])


class CpanelAddbookView(TemplateView):
    # model = category
    template_name = "cpanel/home/content/add-book.html"
    category = category.objects.all().order_by("category")

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"category": self.category})

    def post(self, request, *args, **kwargs):

        if request.POST:
            # declare empty disctionay to pass it later ass save_book() parameter
            form = request.POST
            bookinfo = {}
            BOOKTYPE = []

            bookinfo["title"] = form.get("title")
            bookinfo["author"] = form.get("author")
            bookinfo["quantity"] = form.get("quantity", "")
            bookinfo["category"] = form.get("category")
            bookinfo["description"] = form.get("description")

            if (
                form.get("paperback_price") == ""
                and form.get("audiobook_price") == ""
                and form.get("ebook_price") == ""
            ):
                messages.error(
                    request,
                    "paperback price , audibook price , ebook price can't all be empty . Please fill out at least one ",
                )
                return redirect("cpanel_addbook")

            # get paperback info
            if form.get("paperback_price") != "":
                paperback = {
                    "publisher": form.get("publisher", ""),
                    "publication_date": form.get("publication_date", ""),
                    "language": form.get("language", ""),
                    "isbn_10": form.get("isbn_10", ""),
                    "isbn_13": form.get("isbn_13", ""),
                    "weight": form.get("weight", ""),
                    "dimension": form.get("weight", ""),
                }
                BOOKTYPE.append(
                    {
                        "PAPERBACK": format_book_add(
                            booktype="PAPERBACK",
                            price=form.get("paperback_price"),
                            paperback_details=paperback,
                        )
                    }
                )
            # get audiobook info
            if form.get("audiobook_price") != "":
                audiobook = {
                    "publisher": form.get("audiobook_publisher", ""),
                    "listening_length": form.get("listening_length", ""),
                    "narator": form.get("narator", ""),
                    "realed_date": form.get("realed_date", ""),
                    "Version": form.get("Version", ""),
                    "language": form.get("audiobooklanguage", ""),
                }
                BOOKTYPE.append(
                    {
                        "AUDIOBOOK": format_book_add(
                            booktype="AUDIOBOOK",
                            price=form.get("audiobook_price"),
                            AUDIOBOOK_details=audiobook,
                        )
                    }
                )
            # get ebook info
            if form.get("ebook_price") != "":
                ebook = {
                    "publisher": form.get("ebook_publisher", ""),
                    "language": form.get("ebook_language", ""),
                    "file_size": form.get("file_size", ""),
                    "text_to_speech": form.get("text_to_speech", ""),
                    "screen_reader": form.get("screen_reader", ""),
                    "enhanced_typesetting": form.get("enhanced_typesetting"),
                    "x_Ray": form.get("x_Ray", ""),
                    "word_wise": form.get("word_wise", ""),
                    "print_length": form.get("print_length", ""),
                }
                BOOKTYPE.append(
                    {
                        "EBOOK": format_book_add(
                            booktype="EBOOK",
                            price=form.get("ebook_price"),
                            ebook_details=ebook,
                        )
                    }
                )
            images = request.FILES.getlist("files")
            bookimagespath = {"images": images}
            try:
                save_book(bookinfo, bookimagespath, BOOKTYPE, None)
                messages.success(
                    request, f"{bookinfo['title']} added to database successfully !!"
                )
            except Exception as e:
                messages.error(request, "Error : {e} , Please try again later")

            return HttpResponse("success")

            # hard coded to be changed later
            product_name = "book"
            product_type = "retail"

            booktitle = request.POST["title"]
            author = request.POST["author"]
            quantity = request.POST["quantity"]
            slug = slugify(booktitle)
            images = request.FILES.getlist("files")
            # return HttpResponse("none")
            for index, value in enumerate(request.POST):
                if value in booktype_sample:
                    booktype.update({value: request.POST[value].split(",")})

            if booktype:
                if "PAPERBACK" in booktype:
                    default_price = booktype["PAPERBACK"][1]
                    default_type = booktype["PAPERBACK"][0]
                else:
                    first_element = next(iter(booktype))
                    default_price = booktype[first_element][1]
                    default_type = booktype[first_element][0]

            # create product object
            product = models.product.objects.create(
                product_name=product_name, product_type=product_type
            )
            thumbnail_url = []
            # create images thumbnail
            for index, image in enumerate(images):
                path = os.path.join(BASE_DIR, "media/thumbnail/")
                thumbnail = self.thumbnail(image, path)
                thumbnail_url.append(thumbnail)

            # create book object
            book = models.book.objects.create(
                product=product,
                title=booktitle,
                quantity=quantity,
                author=author,
                slug=slug,
                default_price=default_price,
                default_type=default_type,
                thumbnail=thumbnail_url[0],
            )
            # insert image
            thumbnail_image_url = " ".join(thumbnail_url)
            for i in images:
                models.bookimages.objects.create(
                    book=book,
                    thumbnail=thumbnail_image_url,
                    images=i,
                )

            # insert bookdetials
            for key in booktype:
                models.bookdetails.objects.create(
                    book=book,
                    booktype=key,
                    price=booktype[key][1],
                    description=booktype[key][2],
                )

            messages.success(request, "Book added successfully")

            return JsonResponse({"result": "success"})


class CpanelLogoutVIew(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
        return redirect("cpanel_login")


class CpanelGet_notigication(TemplateView):
    def post(self, request, *args, **kwargs):
        if (
            request.headers.get("x-requested-with") == "XMLHttpRequest"
            and "cpanel_get_notification" in request.POST
        ):
            new_order = models.order.objects.filter(status="pending").count()
            in_progress = models.order.objects.filter(status="confirmed").count()
            data = {"new_order": new_order, "in_progress": in_progress}
            return JsonResponse(data)


class BookFinder(TemplateView):
    template_name = "cpanel/home/content/bookfinder.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = category.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        # print(request.POST)
        if is_ajax(request) and "book_seach" in request.POST:
            booktitle = request.POST.get("title")
            data = search_books(booktitle)
            return JsonResponse({"data": data})
        if is_ajax(request) and "bookinfo" in request.POST:
            BOOKTYPES = []
            bookinfo = json.loads(request.POST["bookinfo"])
            paperback_details = json.loads(request.POST["paperbook_details"])
            ebook_details = json.loads(request.POST["ebook_details"])
            formcheck = json.loads(request.POST["formcheck"])
            form_val = json.loads(request.POST["form_val"])
            # convert serialize form to a dict
            form_values = {}
            for field in form_val:
                form_values[field["name"]] = field["value"]
            image_url = bookinfo.pop("book_thumbnail").replace(
                "zoom=1", "zoom=2"
            )  # pop thumbnial url to download the image
            bookinfo["category"] = form_values["category"]

            # downloaf and process url image
            resp = requests.get(image_url, stream=True)
            if resp.status_code != requests.codes.ok:
                return JsonResponse(
                    {"status": "failed", "val": "failed to download image"}
                )
            fp = BytesIO()
            fp.write(resp.content)
            file_name = image_url.split("/")[
                -1
            ]  # There's probably a better way of doing this but this is just a quick example
            image = files.File(fp)

            # bookimagespath
            bookimagespath = {"images": [image], "file_name": file_name}

            if formcheck["paperbackcheck"]:
                paperback_details["dimensions"] = form_values[
                    "dimensions"
                ]  # add missing field to bookdetials
                paperback_details["weight"] = form_values["book_weight"]
                BOOKTYPES.append(
                    {
                        "PAPERBACK": format_book_add(
                            booktype="PAPERBACK",
                            price=form_values["paperback_price"],
                            paperback_details=paperback_details,
                        )
                    }
                )
            if formcheck["audiobookcheck"]:
                # create audiobook format
                AUDIOBOOK_details = {
                    "author": bookinfo["author"],
                    "publisher": paperback_details["publisher"],
                    "language": paperback_details["language"],
                    "narator": form_values["narator"],
                    "release_date": form_values["release_date"],
                    "version": form_values["version"],
                }
                BOOKTYPES.append(
                    {
                        "AUDIBOOK": format_book_add(
                            booktype="AUDIOBOOK",
                            price=form_values["audibook_price"],
                            AUDIOBOOK_details=AUDIOBOOK_details,
                        )
                    }
                )
            if formcheck["ebookcheck"]:
                ebook_details["publisher"] = paperback_details["publisher"]
                ebook_details["language"] = paperback_details["language"]
                ebook_details["file_size"] = form_values["weight"]
                BOOKTYPES.append(
                    {
                        "EBOOK": format_book_add(
                            booktype="EBOOK",
                            price=form_values["ebook_price"],
                            ebook_details=ebook_details,
                        )
                    }
                )

            # your_model.image_field.save(file_name, files.File(fp))
            try:
                save_book(bookinfo, bookimagespath, BOOKTYPES, form_values)

                messages.success(
                    request, f"{bookinfo['title']} successfully addedd to database !!"
                )
                return JsonResponse({"status": "success"})
            except Exception as e:
                messages.error(
                    request,
                    f"Error: {e}Failed to download book image !! please try different book.",
                )
                return JsonResponse({"status": "failed"})


class DealofWeek(ListView):
    model = models.DealofWeek
    template_name = "cpanel/home/content/dealofweek.html"
    context_object_name = "dealofweek"
    class_form = form.Dealofweek
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.class_form
        return context

    def post(self, request, *args, **kwargs):

        if "book" in request.POST:
            form = self.class_form(request.POST)
            if form.is_valid():
                form.created_by = request.user.email
                form.save()
                messages.success(request, "Deal Created successfully !!")
            else:
                messages.error(
                    request, "Error: Failed to submit form please try again !!"
                )

            return redirect("cpanel_dealofweek")

        if "delete_deal" in request.POST:
            dealid = request.POST.get("delete_deal")
            models.DealofWeek.objects.filter(pk=dealid).delete()
            messages.success(request, "Record deleted successfully !!")
            return redirect("cpanel_dealofweek")

    # def form_valid(self, form):


class OnSale(ListView):
    model = models.book
    template_name = "cpanel/home/content/onsale.html"
    context_object_name = "onsale"


def format_book_add(**bookdetails_info):
    bookFormat = {
        "booktype": bookdetails_info["booktype"],
        "price": float(bookdetails_info["price"]),
        "description": None,
    }
    if bookdetails_info["booktype"] == "PAPERBACK":
        bookFormat["details"] = details_to_string(bookdetails_info["paperback_details"])
    if bookdetails_info["booktype"] == "AUDIOBOOK":
        bookFormat["details"] = details_to_string(bookdetails_info["AUDIOBOOK_details"])
    if bookdetails_info["booktype"] == "EBOOK":
        bookFormat["details"] = details_to_string(bookdetails_info["ebook_details"])

    return bookFormat


def details_to_string(booktype_details_info):
    string = ""
    for key in booktype_details_info:
        string += f"{key} {booktype_details_info[key]};"
    return string


def save_book(bookinfo, bookimagespath, booktypes, form_value):
    # first create book type
    # BOOKTYPE_CHOOSE_DEFUALT = ["PAPERBACK", "AUDIOBOOK", "EBOOK", "HARDCOVER"]
    THUMBNAIL_URL = []
    default_price = 0
    default_booktype = ""

    if "PAPERBACK" in booktypes[0]:
        default_price = booktypes[0]["PAPERBACK"]["price"]
        default_booktype = booktypes[0]["PAPERBACK"]["booktype"]
    else:
        first_element = next(iter(booktypes[0]))
        default_price = booktypes[0][first_element]["booktype"]
        default_booktype = booktypes[0][first_element]["price"]
        # comback here later
    # create product obj
    product = create_product("book", "retail")
    # create_book_image_thumbnail
    for index, image in enumerate(bookimagespath["images"]):
        path = os.path.join(BASE_DIR, "media/thumbnail/")
        THUMBNAIL_URL.append(thumbnail(image, path))

    # create book objc
    book = models.book.objects.create(
        product=product,
        title=bookinfo.get("title"),
        quantity=200,
        author=bookinfo.get("author"),
        slug=slugify(bookinfo.get("title")),
        default_price=float(default_price),
        default_type=default_booktype,
        description=bookinfo.get("description"),
        thumbnail=THUMBNAIL_URL[0],
        category=bookinfo.get("category"),
    )

    # create image obj
    # insert image
    thumbnail_image_url = " ".join(THUMBNAIL_URL)
    for image in bookimagespath["images"]:

        saveimage = models.bookimages.objects.create(
            book=book, thumbnail=thumbnail_image_url, images="randomnameintheboook.wep"
        )
        saveimage.images.save(f"{uuid.uuid4()}_bookimages.webp", image)

    # insert bookdetails
    for detail in booktypes:
        for type in detail:
            models.bookdetails.objects.create(book=book, **detail[type])


def thumbnail(image, path):
    images = Image.open(image)
    MAX_SIZE = (150, 200)
    images.thumbnail(MAX_SIZE)
    image_name = f"{uuid.uuid4()}thumbnail.webp"
    full_name = f"{path}/{image_name}"
    # imag
    images.save(full_name, format="WEBP", quality=90)
    # images.show()
    return image_name


def create_product(product_name, product_type):
    return models.product.objects.create(
        product_name=product_name, product_type=product_type
    )


def is_ajax(request):
    return request.headers.get("x-requested-with") == "XMLHttpRequest"
