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
    template_name = "cpanel/home/content/add-book.html"
    class_form = form.BooksForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"form": self.class_form})

    def post(self, request, *args, **kwargs):

        if request.POST:
            default_price = 0
            default_type = ""
            booktype = {}
            booktype_sample = ["PAPERBACK", "EBOOK", "AUDIOBOOK", "HARDCOVER"]

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
            paperback = json.loads(request.POST["paperbook"])
            ebook = json.loads(request.POST["ebook"])
            form_val = json.loads(request.POST["form_val"])
            # convert serialize form to a dict
            form_values = {}
            for field in form_val:
                form_values[field["name"]] = field["value"]
            image_url = bookinfo.pop("book_thumbnail").replace(
                "zoom=1", "zoom=2"
            )  # pop thumbnial url to download the image
            bookinfo["category"] = form_values["category"]

            print(image_url)

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
            # your_model.image_field.save(file_name, files.File(fp))
            print(files.File(fp))
            return JsonResponse({"j": ";"})

            # bookimagespath
            # try:
            #     images = requests.get(image_url, stream=True)
            #     filename = image_url.split("/")[-1]
            #     tempfile = tempfile.NamedTemporaryFile()
            # except:
            #     pass

            # if request.POST["paperback_check"].get("paperback_check"):
            #     # BOOKTYPES
            #     # frist create product object
            #     product = create_product()
            #     # create_book obje
            #     models.book.objects.create(
            #         product=product,
            #         title=request.POST["bookinfo"].get("title"),
            #         quanity=200,
            #         author=request.POST["bookinfo"].get("author"),
            #         slug=slugify(request.POST["bookinfo"].get("title")),
            #     )
            # save_book(
            #     bookinfo,
            # )

    def format_book_add(self, bookinfo, ebook, bookdetails):
        return {
            "book": "book",
            "booktype": "",
            "price": "price",
            "description": "description",
            "details": "jsonfile",
        }


def save_book(bookinfo, bookdetail, bookimagespath, booktypes):
    # first create book type
    BOOKTYPE_CHOOSE_DEFUALT = ["PAPERBACK", "AUDIOBOOK", "EBOOK", "HARDCOVER"]
    THUMBNAIL_URL = []
    default_price = 0
    default_booktype = ""

    if "PAPERBACK" in booktypes:
        default_price = bookdetail["PAPERBACK"]["price"]
        default_booktype = bookdetail["PAPERNACK"]["type"]
    else:
        pass
        # comback here later
    # create product obj
    product = create_product("book", "retail")

    # create_book_image_thumbnail
    for index, image in enumerate(bookimagespath["images"]):
        path = os.path.join(BASE_DIR, "media/thumbnail/")
        thumbnail = thumbnail(image, path)
        THUMBNAIL_URL.append(thumbnail)

    # create book objc
    book = models.book.objects.create(
        product=product,
        title=bookinfo.get("title"),
        quantity=200,
        author=bookinfo.get("author"),
        slug=slugify(bookinfo.get("title")),
        default_price=default_price,
        default_type=default_booktype,
        thumbnail=bookimagespath.get("thumbnail"),
        category=bookinfo.get("category"),
    )

    # create image obj
    # insert image
    thumbnail_image_url = " ".join(THUMBNAIL_URL)
    for i in bookimagespath["images"]:
        models.bookimages.objects.create(
            book=book,
            thumbnail=thumbnail_image_url,
            images=i,
        )

    # insert bookdetails
    for detail in booktypes:
        detail_ = ""
        for key, value in detail["bookdetails"].tems:
            detail_ += f"{key} {value};"

        models.bookdetails.objects.create(
            book=book,
            booktype=detail["booktype"],
            price=detail["bookprice"],
            description="",
            details=detail_,
        )
    return "done"


def thumbnail(self, image, path):
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
