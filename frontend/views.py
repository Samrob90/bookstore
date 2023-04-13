from django.shortcuts import render, redirect
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
from datetime import date, datetime
import time
from django.db.models import Sum
import random, string
from rsc.tools import timer
from .context import grabe_children
from django.db.models import F
from . import form


class HomeVIew(ListView):
    template_name = "frontend/home.html"
    model = cpanel_model.book
    context_object_name = "books"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # best sellers books
        context["best_seller"] = cpanel_model.order_book.objects.all().order_by(
            "-bookquantity"
        )[:10]

        # booksonsale
        context["onsales"] = cpanel_model.OnSale.objects.filter(
            periode__gt=datetime.now()
        ).order_by("-created_at")
        # deal of week
        context["dealofweek"] = cpanel_model.DealofWeek.objects.filter(
            periode__gt=datetime.now()
        ).order_by("-created_at")

        context["selfhelp"] = cpanel_model.book.objects.filter(
            category__contains="SELF-HELP"
        ).order_by("-created_at")[:10]

        # authors
        context["authors"] = cpanel_model.Authors.objects.all().order_by("-created_at")[
            :10
        ]
        return context

    def get_queryset(self):
        return cpanel_model.book.objects.all().order_by("created_at")[:12]


class authorsDetail(DetailView):
    model = cpanel_model.Authors
    template_name = "frontend/author_single.html"
    context_object_name = "author"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["author_books"] = cpanel_model.book.objects.filter(
            author=self.model.fullname
        )
        print(context)
        return context


# change to list view when model is ready
class ShopView(ListView):
    template_name = "frontend/shop.html"
    model = cpanel_model.book
    context_object_name = "books"

    paginate_by = 20
    ordering = ["-created_at"]

    def get_queryset(self):
        sortby = self.request.GET.get("sort", None)
        best_seller = self.request.GET.get("bestsellers", None)
        category = self.request.GET.get("category", None)
        sub = self.request.GET.get("sub", None)
        the_request = self.request.GET
        # should probably find a better way to minimize this code
        if "format" in the_request:
            category = the_request.get("category")
            filter_format = the_request.get("format")

            return cpanel_model.book.objects.filter(
                category__contains=category, bookdetails__booktype=filter_format
            )

        if best_seller is not None:
            bestseller = cpanel_model.order_book.objects.all().order_by(
                "-bookquantity"
            )[:20]
            return bestseller
        elif sub is not None:
            # first fetch sub category model
            sub_obj = models.subcategory.objects.filter(subcategory__contains=sub)
            # then get category from subcatero
            category = sub_obj.category
            # return category related books
            return cpanel_model.book.objects.filter(category__contains=category[0:10])
        elif category is not None:
            return cpanel_model.book.objects.filter(category__contains=category)[0:10]
        elif sortby is not None:
            pass
        else:
            return super().get_queryset()


class CategoriesView(ListView):
    template_name = "frontend/categories.html"
    model = models.category
    context_object_name = "categories"


class ProductView(DetailView):
    template_name = "frontend/product_single.html"
    model = cpanel_model.book
    context_object_name = "book"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        # if self.kwargs["type"]:
        #     book_default_type = self.kwargs["type"]
        #     default_book_id = self.kwargs["uuid"]
        #     context["book_default_details"] = cpanel_model.bookdetails.objects.filter(
        #         book=book, booktype=book_default_type
        #     ).first()

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
        if "bookdetails_page" in request.POST:
            print(request.POST)
            Qty = request.POST.get("quantity")
            bookid = request.POST.get("book_id")
            book_type_info = request.POST.get("booktype_price").split(" ")
            booktype = book_type_info[0]
            bookprice = book_type_info[1]
            bookpk = request.POST.get("bookpk")
            # product = cpanel_model.product.objects.get(product_id=bookid)
            book = cpanel_model.book.objects.get(pk=bookpk)
            cart = {
                "product_id": bookid,
                "booktitle": book.title,
                "bookquantity": Qty,
                "bookthumbnail": book.thumbnail,
                "bookprice": float(bookprice),
                "booktype": booktype,
                "bookauthor": book.author,
                "bookslug": book.slug,
            }
            result = self.store_cart(request, cart)
            messages.success(request, f"{book.title}. Added to your cart successfully ")
            return redirect("book-detail", book.slug, bookid)
            # print(result)

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

        # update book quanity in cart page
        if self.is_ajax(request) and "cart_update_qty" in request.POST:
            qty = request.POST.get("cart_update_qty")
            bookid = request.POST.get("bookid")

            # check if user is authenticated
            if request.user.is_authenticated:
                # update cart model
                models.cart.objects.filter(product_id=bookid, user=request.user).update(
                    bookquantity=qty
                )
            else:
                # get current book to update
                book_stored = request.session["cart"][bookid]
                book_stored["bookquantity"] = qty
                request.session, modified = True
            if "keypress" in request.POST:
                messages.success(request, "Cart updated successfully !!")
            return JsonResponse({"result": "success"})

    # check if request is ajax
    def is_ajax(self, request):
        return request.headers.get("x-requested-with") == "XMLHttpRequest"

    # store cart to session or db
    def store_cart(self, request, data, add_to_recent_view=False):
        if request.user.is_authenticated:
            # check if the same cart already existe in db
            cart_id = models.cart.objects.filter(
                product_id=data["product_id"],
                booktype=data["booktype"],
                user=request.user,
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
            "bookprice": float(book.default_price),
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
    form_class = form.ContactForm()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contact_us"] = cpanel_model.general_settings.objects.all().first()
        context["form"] = form.ContactForm()
        return context

    def post(self, request, *args, **kwargs):
        form_obj = form.ContactForm(request.POST)
        if form_obj.is_valid():
            form_obj.save()
            messages.success(
                request,
                "Thank you for your feedback , your message has been succeesfully sent !!",
            )
            tasks.send_to_support(form_obj.pop)
            # return redirect("contact")
        else:
            # for error in form_obj.errors.items():
            messages.error(request, "Error!! Please make sure you fill all field .")
        return redirect("contact")


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


# checkout


class CheckoutView(TemplateView):
    template_name = "frontend/checkout.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["addresses"] = cpanel_model.Addresse.objects.filter(
                user=self.request.user.email
            ).order_by("-created_at")[0:3]
        return context

    # recalculate here before production
    @timer
    def post(self, request, *args, **kwargs):
        # ajax call calculate shipping cost
        if self.is_ajax(request) and "calculate_shipping_cost" in request.POST:
            addressid = request.POST.get("addressid")
            address = cpanel_model.Addresse.objects.filter(pk=addressid).first()
            shipping_cost = self.shipping_calculator(address.country, address.city)
            return JsonResponse({"result": shipping_cost})
        # proccess payment request
        if self.is_ajax(request) and "checkout" in request.POST:
            coupon = None
            sub_total = 0
            address = None
            addressid = request.POST.get("addressid")
            couponcode = str(request.POST.get("coupon_code1"))
            payment_method = str(request.POST.get("payment_method"))
            email = ""
            shipping_address = None
            data = dict()
            address_type = request.POST.get("address_type")
            items = []

            if request.user.is_authenticated:
                # get cart sub_toal
                cart_obj = models.cart.objects.filter(user=request.user)
                for i in cart_obj:
                    sub_total += float(i.bookquantity) * float(i.bookprice)
                    items.append(model_to_dict(i))
            else:
                list = grabe_children(request.session["cart"])
                sub_total = list[1]
                for i in list[0]:
                    items.append(i)

            # check if addressid is not underfined
            if addressid is not None and request.user.is_authenticated:
                email = request.user.email

                shipping_address = cpanel_model.Addresse.objects.filter(
                    pk=addressid
                ).first()
            elif addressid is None and request.user.is_authenticated:
                email = request.user.email
                shipping_address = self.get_address(request)
                addressid = 0
                address_type = "user_new_address"

            else:
                email = request.POST.get("billing_email")
                shipping_address = self.get_address(request)

                # get cart total and cart content from value

            # check if coupon existe and get coupon code cariblar
            if couponcode != "" or couponcode is not None:
                coupon_obj = cpanel_model.coupon.objects.filter(code=couponcode)
                if coupon_obj.exists():
                    coupon = coupon_obj.first()
            total = self.get_total(shipping_address, sub_total, coupon)
            Ordernumner = "".join(random.choices(string.digits, k=10))

            # should check this code before production

            if request.user.is_authenticated and addressid is not None:
                shipping_address = None

            data["orderid"] = Ordernumner
            data["email"] = email
            data["items"] = items
            data["addressid"] = addressid
            data["address"] = shipping_address
            data["payment_method"] = payment_method
            data["address_type"] = address_type
            data["coupon"] = couponcode
            data["shipping_fee"] = total[1]
            data["discount"] = total[2]
            data["total"] = total[0]

            if payment_method == "pay_with_momo":
                # make api call here
                pass
            else:
                # send data to task to save
                tasks.save_order.delay(data)
                # delete session if existe
                if "cart" in request.session:
                    del request.session["cart"]
                    request.session.modified = True

                return JsonResponse({"result": "success", "orderNumber": Ordernumner})

            # send total and address and payment_method to task

            # calculate shipping fees

        # if coupon_percentage != 0 :

        # ajax call check if coupon code is still valide
        if self.is_ajax(request) and "coupon_code_check" in request.POST:
            coupon = request.POST.get("coupon")
            total = request.POST.get("total")
            coupon_obj = cpanel_model.coupon.objects.filter(code=coupon)
            # time.sleep(5)
            if coupon_obj.exists():
                result = self.coupon_calculator(coupon_obj.first(), total)
                if result == "invalide":
                    return JsonResponse({"result": "Expired"})
                else:
                    return JsonResponse(
                        {
                            "result": "valid",
                            "total": result[0],
                            "discount": result[1],
                            "percentage": result[2],
                        }
                    )
            else:
                return JsonResponse({"result": "invalide"})

    def get_address(self, request):
        if request.user.is_authenticated:
            email = request.user.email
        else:
            email = request.POST.get("billing_email")
        return {
            "first_name": request.POST.get("billing_first_name"),
            "last_name": request.POST.get("billing_last_name"),
            "country": request.POST.get("billing_country"),
            "address1": request.POST.get("billing_address_1"),
            "address2": request.POST["billing_address_2"],
            "city": request.POST.get("billing_city"),
            "state": request.POST.get("billing_state"),
            "number": request.POST.get("billing_phone"),
            "email": email,
        }

    def get_total(self, address, sub_total, coupon_obj):
        try:
            country = address.country
            city = address.city
        except:
            country = address["country"]
            city = address["city"]
        Total = 0
        shipping_cost = 0
        discount = 0
        # get shipping fees
        if sub_total >= 300:
            shipping_cost = 0
        else:
            shipping_cost = float(self.shipping_calculator(country, city))
        subtotal = shipping_cost + sub_total  # add sub_total to shipping cost
        if coupon_obj is not None:  # check is coupon is not empty
            coupon_response = self.coupon_calculator(coupon_obj, subtotal)
            if coupon_response == "invalide":
                Total = subtotal
            else:
                Total = coupon_response[0]
                discount = coupon_response[1]
        else:
            Total = subtotal

        return [Total, shipping_cost, discount]

    def order_format(self, data):
        return {
            "email": data.email,
            "items": data.items,
            "address": data.address,
            "payment_method": data.payment_method,
        }

    def coupon_calculator(self, coupon_obj, total):
        coupon_percentage = coupon_obj.percentage
        coupon_expiration_time = coupon_obj.expires_on
        if timezone.now() <= coupon_expiration_time:
            discount = float((int(total) * int(coupon_percentage)) / 100)
            new_total = float(total) - discount
            return [new_total, discount, coupon_percentage]
        else:
            return "invalide"

    def shipping_calculator(self, country, city):
        shipping_cost = 0
        if country.lower() == "ghana":
            if city.lower() == "accra":
                shipping_cost = 35
            elif city.lower == "tema":
                shipping_cost = 50
            else:
                shipping_cost = 60

        else:
            shipping_cost = 455
        return shipping_cost

    def is_ajax(self, request):
        return request.headers.get("x-requested-with") == "XMLHttpRequest"


# cart


def OrderSuccess(request, ordernumber):
    # template_name = "frontend/ordersuccess.html"
    # model = cpanel_model.order
    # context_object_name = "order"
    if request.method == "GET":
        context = {"ordernumber": ordernumber}
        return render(request, "frontend/ordersuccess.html", context)


# class storeCart:
#     def __init__(self, data) -> None:


class bookReview(TemplateView):
    def post(self, request, *args, **kwargs):
        if self.is_ajax(request) and "book_review" in request.POST:
            time.sleep(2)
            ratings = request.POST.get("rating")
            commet = request.POST.get("commet")
            bookid = request.POST.get("bookid")
            title = request.POST.get("review_title")
            book = cpanel_model.book.objects.filter(pk=bookid).first()

            cpanel_model.ratings.objects.create(
                user=request.user,
                book=book,
                stars=int(ratings),
                title=title,
                comments=commet,
            )
            return JsonResponse({"status": "success"})

        # likes
        # if self.is_ajax(request) and "review_likes" in request.POST:
        #     review_type = request.POST.get("review_likes")
        #     bookid = request.POST.get("bookid")
        #     type = request.POST.get("status")
        #     oposite = request.POST.get("oposite")
        #     commentid = request.POST.get("commentid")

        #     comment = cpanel_model.ratings.objects.get(pk=commentid)
        #     check = cpanel_model.UserLikes.objects.filter(
        #         ratings=comment, user=request.user
        #     )
        #     # check back here with clear mind
        #     if check.exists():
        #         pass
        #     else:

        #         cpanel_model.ratings.objects.filter(pk=commentid).update(
        #             likes=F(str(review_type)) + 1
        #         )
        #         # comment.update(likes=F(str(review_type)) + 1)
        #         cpanel_model.UserLikes.objects.update_or_create(
        #             user=request.user,
        #             ratings=comment,
        #             defaults={"liked": True, "disliked": False},
        #         )
        #         if type == True:
        #             cpanel_model.ratings.objects.filter(pk=commentid).update(
        #                 likes=F(str(oposite)) + 1
        #             )
        #             # create a function for this particular post
        #             # temporary fixe
        #             cpanel_model.UserLikes.objects.update_or_create(
        #                 user=request.user,
        #                 ratings=comment,
        #                 # liked=True,
        #                 # disliked=False,
        #                 defaults={"liked": False, "disliked": True},
        #             )

        #     return JsonResponse({"status": "done"})

    # likes

    def is_ajax(self, request):
        return request.headers.get("x-requested-with") == "XMLHttpRequest"

    # all reviews


class RatingsView(DetailView):
    model = cpanel_model.book
    template_name = "frontend/ratings.html"
    context_object_name = "comments"
    # queryset = cpanel_model.ratings.objects.filter(book=self.pk)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context[""] = "none"
    #     return context

    # def get_queryset(self, *args, **kwargs):
    #     book = cpanel_model.book.objects.filter(pk=kwargs["pk"])
    #     return self.model.objects.filter(book=book).order_by("-created_at")
