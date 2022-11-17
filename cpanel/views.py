from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from . import form
from django.contrib.auth import authenticate, login, logout
from authentications.models import Account
from django.contrib import messages
from django.http import HttpResponse
from . import models
from PIL import Image
from random import Random, random
from bookstore.settings import BASE_DIR
import uuid, os, json
from django.template.defaultfilters import slugify

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


class CpanelBooksView(TemplateView):
    template_name = "cpanel/home/content/book.html"


class CpanelAddbookView(TemplateView):
    template_name = "cpanel/home/content/add-book.html"
    class_form = form.BooksForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"form": self.class_form})

    def post(self, request, *args, **kwargs):

        if request.POST:
            default_price = 0
            default_type = ""
            booktype = []
            booktype_sample = ["PAPERBACK", "EBOOK", "AUDIOBOOK", "HARDCOVER"]

            # hard coded to be changed later
            product_name = "book"
            product_type = "retail"

            booktitle = request.POST["title"]
            author = request.POST["author"]
            quantity = request.POST["quantity"]
            slug = slugify(booktitle)
            images = request.FILES.getlist("files")

            for index, value in enumerate(request.POST):
                if value in booktype_sample:
                    booktype.append({value: request.POST[value]})

            if booktype:
                default_price = booktype[0][1]
                default_type = booktype[0][0]

            # create product object
            product = models.product.objects.create(
                product_name=product_name, product_type=product_type
            )
            thumbnail_url = []
            # create images thumbnail
            for index, image in enumerate(images):
                path = os.path.join(BASE_DIR, "media/thumbnail/")
                thumbnail = thumbnail(image, path)
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
            for i in image:
                models.bookimages.objects.create(
                    book=book,
                    thumbnail=thumbnail_image_url,
                    images=i,
                )

            return HttpResponse("done")

    def thumbnail(self, image, path):
        images = Image.open(image)
        MAX_SIZE = (150, 200)
        images.thumbnail(MAX_SIZE)
        image_name = f"{uuid.uuid4()}thumbnail.webp"

        full_name = f"{path}/{image_name}"
        # imag
        images.save(full_name)
        # images.show()
        return image_name


class CpanelLogoutVIew(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
        return redirect("cpanel_login")
