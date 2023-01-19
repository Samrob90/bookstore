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

# from random import Random, random
from bookstore.settings import BASE_DIR
import uuid, os
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

        # redirect to omplete order page


class CompletedOrder(ListView):
    model = models.order
    template_name = "cpanel/home/content/order_completed.html"
    context_object_name = "cpanel_order_completed"
    paginate_by = 20

    def get_queryset(self):
        unwamted_fields = ["pending", "confirmed"]
        return self.model.objects.exclude(status__in=[o for o in unwamted_fields])


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
            print(thumbnail)
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
