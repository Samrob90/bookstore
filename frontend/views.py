from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from cpanel import models as cpanel_model
from math import ceil
from django.http import HttpResponse, JsonResponse
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from django.contrib import messages


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

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            return HttpResponse("hello world")
        # Qty = request.POST["quantity"]
        # product_id = kwargs["uuid"]
        # product = cpanel_model.product.objects.get(product_id=product_id)
        # book = cpanel_model.book.objects.get(product=product)
        # book_detail = cpanel_model.bookdetails.objects.get(
        #     book=book, booktype=kwargs["type"]
        # )

        # cart = {
        #     "product_id": kwargs["uuid"],
        #     "book_title": book.title,
        #     "book_quantity": Qty,
        #     "book_thumbnail": book.thumbnail,
        #     "book_price": book_detail.price,
        #     "book_type": book_detail.booktype,
        # }
        # result = self.store_cart(request, cart)
        # if result:
        #     messages.success(request, f"{{book.title}} added to cart ")
        # # context =
        # # return render(
        # #     request, self.template_name, context=self.get_context_data(kwargs)
        # # )


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
            }
            result = self.store_cart(request, cart)
            if result:
                messages.success(request, f"{book.title} added to cart successfully !")
                return JsonResponse({"result": "success"})
            else:
                return JsonResponse({"result": "failed"})

    def is_ajax(self, request):
        return request.headers.get("x-requested-with") == "XMLHttpRequest"

    def store_cart(self, request, data, add_to_recent_view=False):
        if request.user.is_authenticated:
            pass
        else:
            if "cart" in request.session:
                session = request.session["cart"]
                # is this product already in cart session increase book quantiy
                if str(data["product_id"]) in request.session["cart"]:
                    session_product_data = session[str(data["product_id"])]
                    # check if book type is the same

                    # print(len(session_product_data))
                    for index, value in enumerate(session_product_data, start=0):
                        if value["book_type"] == data["book_type"]:
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
                    request.session["cart"][str(data.product_id)] = data
            else:
                cart_session = request.session["cart"] = {}
                cart_session[str(data["product_id"])] = [data]
                request.session.modifed = True
            return True


class AboutView(TemplateView):
    template_name = "frontend/about.html"


class ContactView(TemplateView):
    template_name = "frontend/contact.html"


class FaqView(TemplateView):
    template_name = "frontend/faq.html"


# cart


# class storeCart:
#     def __init__(self, data) -> None:
