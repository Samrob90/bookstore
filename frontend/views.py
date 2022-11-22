from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from cpanel import models as cpanel_model
from math import ceil
from django.http import HttpResponse, JsonResponse
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from django.contrib import messages
from . import models
from django.utils import timezone


class HomeVIew(TemplateView):
    template_name = "frontend/home.html"


# change to list view when model is ready
class ShopView(ListView):
    template_name = "frontend/shop.html"
    model = cpanel_model.book
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["range"] = range(
            1, ceil(cpanel_model.book.objects.all().count() / 4) + 1
        )
        return context


class ProductView(DetailView):
    template_name = "frontend/product_single.html"
    model = cpanel_model.book
    context_object_name = "book"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        if self.kwargs["type"]:
            book_default_type = self.kwargs["type"]
            default_book_id = self.kwargs["uuid"]
            context["book_default_details"] = cpanel_model.bookdetails.objects.filter(
                book=book, booktype=book_default_type
            ).first()
        details = cpanel_model.bookdetails.objects.filter(book=book)
        context["book_images"] = cpanel_model.bookimages.objects.filter(book=book)
        context["details"] = details
        context["booktype__"] = [self.kwargs["type"], details.first().price]

        return context


class shopCart(TemplateView):
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        if self.is_ajax(request) and "bookdetails_page" in request.POST:
            Qty = request.POST.get("quantity")
            bookid = request.POST.get("book_id")
            booktype = request.POST.get("book_type")
            bookprice = request.POST.get("book_price")
            product = cpanel_model.product.objects.get(product_id=bookid)
            book = cpanel_model.book.objects.get(product=product)
            cart = {
                "product_id": bookid,
                "book_title": book.title,
                "book_quantity": Qty,
                "book_thumbnail": book.thumbnail,
                "book_price": bookprice,
                "book_type": booktype,
                "book_author": book.author,
                "book_slug": book.slug,
            }
            result = self.store_cart(request, cart)
            if result:
                messages.success(request, f"{book.title} added to cart successfully !")
                return JsonResponse({"result": "success"})
            else:
                return JsonResponse({"result": "failed"})

        # remove cart from session
        if self.is_ajax(request) and "removeCartItem" in request.POST:
            product_id = request.POST.get("product_id")
            booktype = request.POST.get("booktype")
            print(product_id)
            if request.user.is_authenticated:
                pass
            else:
                if request.session["cart"]:

                    if product_id in request.session["cart"]:
                        for index, value in enumerate(
                            request.session["cart"][str(product_id)]
                        ):
                            if (
                                value["book_type"] == booktype
                                and product_id == value["product_id"]
                            ):
                                if len(request.session["cart"][str(product_id)]) == 1:
                                    del request.session["cart"][str(product_id)]
                                else:
                                    request.session["cart"][str(product_id)].pop(index)
                                request.session.modified = True
                                messages.info(
                                    request, "Product remove from cart successfuly"
                                )
                                return JsonResponse({"result": "success"})

    def is_ajax(self, request):
        return request.headers.get("x-requested-with") == "XMLHttpRequest"

    def store_cart(self, request, data, add_to_recent_view=False):
        if request.user.is_authenticated:
            pass
        else:
            if "cart" in request.session:
                session = request.session["cart"]
                # del request.session["cart"]
                # request.session.modified = True
                # return
                print(session)

                # return None
                # is this product already in cart session increase book quantiy
                if str(data["product_id"]) in request.session["cart"]:
                    session_product_data = session[str(data["product_id"])]
                    # check if book type is the same

                    # print(len(session_product_data))
                    if len(session_product_data) > 0:
                        for index, value in enumerate(session_product_data, start=0):
                            if value:
                                print("there is value")
                            else:
                                print("no value here")
                            if (
                                value["book_type"] == data["book_type"]
                                and value["product_id"] == data["product_id"]
                            ):
                                # local data copie
                                new_data = data

                                current_dict = int(value["book_quantity"])
                                # del session_product_data[index]
                                session_product_data.pop(index)
                                data.update(
                                    {
                                        "book_quantity": current_dict
                                        + int(new_data["book_quantity"])
                                    }
                                )
                                session_product_data.insert(index, new_data)

                                request.session.modified = True
                                # print(session_product_data)
                            else:
                                session_product_data.append(data)
                                request.session.modified = True
                    else:
                        print("in herer")
                        session_product_data.append(data)
                        request.session.modified = True

                else:
                    request.session["cart"][str(data["product_id"])] = [data]
                    request.session.modified = True
            else:
                cart_session = request.session["cart"] = {}
                cart_session[str(data["product_id"])] = [data]
                request.session.modified = True
            return True


class AboutView(TemplateView):
    template_name = "frontend/about.html"


class ContactView(TemplateView):
    template_name = "frontend/contact.html"


class FaqView(TemplateView):
    template_name = "frontend/faq.html"


class CartViews(TemplateView):
    model: models.cart
    template_name = "frontend/cart.html"
    context_object_name = "cart_page"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["now"] = timezone.now()
        return context


# cart


# class storeCart:
#     def __init__(self, data) -> None:
