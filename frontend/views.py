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
import json
from django.forms.models import model_to_dict
from . import tasks


class HomeVIew(TemplateView):
    template_name = "frontend/home.html"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)


# change to list view when model is ready
class ShopView(ListView):
    template_name = "frontend/shop.html"
    model = cpanel_model.book
    paginate_by = 5

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

        data = {
            "product_id": str(book.product.product_id),
            "booktitle": book.title,
            "bookquantity": 1,
            "bookthumbnail": book.thumbnail,
            "bookprice": float(book.default_price),
            "booktype": book.default_type,
            "bookauthor": book.author,
            "bookslug": book.slug,
        }

        if self.request.user.is_authenticated:

            tasks.save_recent.delay(self.request.user.pk, data)
            recent_view = models.recent_viewied_item.objects.filter(
                user=self.request.user
            ).order_by("-created_at")[:9]
        else:
            recent_view = self.set_recent_session(self.request, data)
        context["recent_view"] = recent_view

        return context

    def set_recent_session(self, request, data):
        if "recent_view" in request.session:
            session_value = request.session["recent_view"]
            # check if this item is already in session
            # print(session_value[0])

            if len(session_value) <= 9:
                for index, value in enumerate(session_value):
                    # print(index, value)
                    if str(data["product_id"]) == str(value["product_id"]):
                        session_value.pop(index)

            if len(session_value) >= 9:
                session_value.pop()
            session_value.insert(0, data)
        else:
            request.session["recent_view"] = [data]

        request.session.modified = True
        return request.session["recent_view"]


class shopCart(TemplateView):
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        if self.is_ajax(request) and "bookdetails_page" in request.POST:
            Qty = request.POST.get("quantity")
            bookid = request.POST.get("book_id")
            print(bookid)
            booktype = request.POST.get("book_type")
            bookprice = request.POST.get("book_price")
            print(bookprice)
            product = cpanel_model.product.objects.get(product_id=bookid)
            book = cpanel_model.book.objects.get(product=product)
            cart = {
                "product_id": bookid,
                "booktitle": book.title,
                "bookquantity": Qty,
                "bookthumbnail": book.thumbnail,
                "bookprice": bookprice,
                "booktype": booktype,
                "bookauthor": book.author,
                "bookslug": book.slug,
            }
            result = self.store_cart(request, cart)
            if result:
                messages.success(
                    request, f"{book.title}. Added to your cart successfully "
                )
                return JsonResponse({"result": "success"})
            else:
                return JsonResponse({"result": "failed"})

        # add to cart from shop page
        if self.is_ajax(request) and "shop_add_top_cart" in request.POST:
            action_type = request.POST.get("shop_add_top_cart")
            product_id = request.POST.get("product_id")
            product = cpanel_model.product.objects.get(product_id=str(product_id))
            book = cpanel_model.book.objects.get(product=product)
            cart = self.cart_format(book)

            if action_type == "cart":
                result = self.store_cart(request, cart)
                # return cart
                if request.user.is_authenticated:
                    cart_ = model_to_dict(
                        models.cart.objects.get(product_id=product_id)
                    )
                else:
                    cart_ = request.session["cart"][str(product_id)][0]
                if result:
                    return JsonResponse({"result": cart_})
                else:
                    return JsonResponse({"result": "failed"})
            else:
                # store item in wishlist
                if request.user.is_authenticated:
                    product_id = request.POST.get("product_id")
                    product = cpanel_model.product.objects.get(product_id=product_id)
                    book = cpanel_model.book.objects.get(product=product)
                    wishlist = self.cart_format(book)
                    db_format = self.change_cart_dormat_to_db_format(
                        request.user, wishlist
                    )

                    result = self.store_wishlist(request, db_format)
                    obj = model_to_dict(
                        models.wishlist.objects.get(product_id=product_id)
                    )
                    if not result:
                        return JsonResponse({"result": "failed", "data": obj})
                    else:
                        return JsonResponse({"result": "success", "data": obj})
                else:
                    return JsonResponse({"result": "notauth"})

        # store in wish list from detailspage (This section should be removed with improving the code )
        if self.is_ajax(request) and "add_to_wishlist_bookdetails_page" in request.POST:
            bookid = request.POST.get("bookid")
            book = cpanel_model.book.objects.get(pk=bookid)
            # check if this book already existe in wishlist
            wishlist = self.cart_format(book)
            db_format = self.change_cart_dormat_to_db_format(request.user, wishlist)
            result = self.store_wishlist(request, db_format)
            if result:
                messages.success(request, f"{book.title}. added to your wishlist")
                return JsonResponse({"result": "success"})
            else:
                messages.error(request, f"{book.title}. is already in your wishlist")
                return JsonResponse({"result": "failed"})

        # remove cart
        if self.is_ajax(request) and "removeCartItem" in request.POST:
            product_id = request.POST.get("product_id")
            booktype = request.POST.get("booktype")
            # remove cart from  database
            if request.user.is_authenticated:
                delete = models.cart.objects.filter(
                    user=request.user, product_id=product_id, booktype=booktype
                )
                book_title = delete.first().booktitle
                delete.delete()

                messages.info(request, f"{book_title}")
                return JsonResponse({"result": "success"})

            else:
                # remove cart from session
                if request.session["cart"]:

                    if product_id in request.session["cart"]:
                        for index, value in enumerate(
                            request.session["cart"][str(product_id)]
                        ):
                            if (
                                value["booktype"] == booktype
                                and product_id == value["product_id"]
                            ):
                                product_title = request.session["cart"][
                                    str(product_id)
                                ][0]["booktitle"]
                                if len(request.session["cart"][str(product_id)]) >= 1:
                                    del request.session["cart"][str(product_id)]
                                else:
                                    request.session["cart"][str(product_id)].pop(index)
                                request.session.modified = True
                                messages.info(request, f"{product_title}")
                                return JsonResponse({"result": "success"})

    # check if request is ajax
    def is_ajax(self, request):
        return request.headers.get("x-requested-with") == "XMLHttpRequest"

    # store cart to session or db
    def store_cart(self, request, data, add_to_recent_view=False):
        if request.user.is_authenticated:
            # check if the same cart already existe in db
            cart_id = models.cart.objects.filter(
                product_id=data["product_id"], booktype=data["booktype"]
            )
            if cart_id.exists():
                # increase book quanitty if book already existe in db
                quantity = int(cart_id.first().bookquantity) + int(data["bookquantity"])
                cart_id.update(bookquantity=quantity)
                return True

            else:
                # print(data)
                models.cart.objects.create(
                    user=request.user,
                    product_id=data["product_id"],
                    booktitle=data["booktitle"],
                    bookquantity=data["bookquantity"],
                    bookthumbnail=data["bookthumbnail"],
                    bookprice=data["bookprice"],
                    booktype=data["booktype"],
                    bookauthor=data["bookauthor"],
                    bookslug=data["bookslug"],
                )
                return True

        else:
            if "cart" in request.session:
                session = request.session["cart"]
                # is this product already in cart session increase book quantiy
                if str(data["product_id"]) in request.session["cart"]:

                    session_product_data = session[str(data["product_id"])]
                    # check if book type is the same
                    if len(session_product_data) > 0:
                        for index, value in enumerate(session_product_data, start=0):
                            if (
                                value["booktype"] == data["booktype"]
                                and value["product_id"] == data["product_id"]
                            ):
                                # local data copie

                                current_dict = int(value["bookquantity"]) + int(
                                    data["bookquantity"]
                                )
                                print(current_dict)

                                # del session_product_data[index]
                                session_product_data.pop(index)
                                request.session.modified = True
                                data.update({"bookquantity": current_dict})
                                session_product_data.insert(index, data)

                                request.session.modified = True
                                # print(session_product_data)
                            else:
                                session_product_data.append(data)
                                request.session.modified = True
                    else:
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

    def store_wishlist(self, request, data):
        # check if item exist in wishlist
        item_in_wishlist = models.wishlist.objects.filter(
            user=request.user, product_id=data["product_id"]
        )
        if item_in_wishlist.exists():
            return False
        else:
            models.wishlist.objects.create(**data)
            return True

    def cart_format(self, book):
        return {
            "product_id": str(book.product.product_id),
            "booktitle": book.title,
            "bookquantity": 1,
            "bookthumbnail": book.thumbnail,
            "bookprice": book.default_price,
            "booktype": book.default_type,
            "bookauthor": book.author,
            "bookslug": book.slug,
        }

    def change_cart_dormat_to_db_format(self, user, cart):
        db_format = {"user": user}
        for key, value in cart.items():
            if key == "product_id":
                db_format[key] = value
            elif key == "bookquantity":
                continue
            else:
                db_format[key] = value

        return db_format


class AboutView(TemplateView):
    template_name = "frontend/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["about"] = models.about_us.objects.all().first()
        return context


class ContactView(TemplateView):
    template_name = "frontend/contact.html"


class FaqView(ListView):
    template_name = "frontend/faq.html"
    model = models.faq
    context_object_name = "faq"


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
