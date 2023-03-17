from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from frontend.models import wishlist as frontend_wishlist
from cpanel.models import order, Addresse, Account
from frontend.models import wishlist, cart
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.views.generic.detail import DetailView
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password


# Create your views here.
class AccountHomeView(TemplateView):
    template_name: str = "frontend/account/dashboard.html"


class OrderView(ListView):
    model = order
    template_name: str = "frontend/account/orders.html"
    context_object_name = "account_orders"
    paginate_by = 20
    ordering = ["-created_at"]
    # queryset = model.

    def get_queryset(self):
        return order.objects.filter(email=self.request.user.email).order_by(
            "-created_at"
        )[0:20]


class order_account_details(TemplateView):
    template_name = "frontend/account/order_account_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order"] = order.objects.filter(orderid=context["orderid"]).first()
        return context

    # def get_queryset(self):
    #     print(self.context)
    #     # return order.objects.filter(orderid=kwargs["orderid"])


class DownloadsView(TemplateView):
    template_name: str = "frontend/account/downloads.html"


class AddressesView(ListView):
    model = Addresse
    template_name: str = "frontend/account/addresses.html"
    context_object_name = "address"

    def get_queryset(self):
        return Addresse.objects.filter(user=self.request.user.email).order_by(
            "-created_at"
        )

    def post(self, request, *args, **kwargs):
        if "submit_user_form_change" in request.POST:
            # return JsonResponse(request.POST)
            # update user purchase address
            Addresse.objects.filter(pk=request.POST.get("addressid")).update(
                first_name=request.POST.get("billing_first_name"),
                last_name=request.POST.get("billing_last_name"),
                address1=request.POST.get("billing_address_1"),
                address2=request.POST.get("billing_address_2"),
                country=request.POST.get("billing_country"),
                region_or_state=request.POST.get("billing_state"),
                city=request.POST.get("billing_city"),
                phonenumber=request.POST.get("billing_phone"),
            )
            messages.success(request, "Address updated successfully !!")
            return redirect("addresses")


class AccountDetails(TemplateView):
    template_name: str = "frontend/account/account-detailes.html"

    def post(self, request, *args, **kwargs):
        if "user_change_password" in request.POST:
            current_password = request.POST.get("currentpassword")
            new_password = request.POST.get("newpassword")
            confirm_new_password = request.POST.get("confirmnewpassword")

            # check is current password macthes with stored password
            if check_password(current_password, request.user.password):
                if new_password != confirm_new_password:
                    messages.error(request, "Passwords do not match")
                else:
                    new_password2 = make_password(new_password, hasher="default")
                    user = Account.objects.get(pk=request.user.pk)
                    user.set_password(new_password)
                    user.save()
                    messages.success(
                        request,
                        "Your password has been changed successfully !! Please login with your new password",
                    )

            else:
                messages.error(
                    request, "Current password is invalid . Please try again"
                )

            return redirect("profile")

        if "user_change_password" in request.POST:
            delete = Account.objects.filter(user=request.user).delete()
            messages.success(
                request, "Success !! Your account has been deleted successfuly ."
            )
            return redirect("profile")

        # update user information

        if "update_user_profile" in request.POST:
            first_name = request.POST.get("firstname")
            last_name = request.POST.get("lastname")
            email = request.POST.get("email")

            # if first_name == request.user.first_name and last_name == request.user.last_name  and email == request.user.email:
            #     messages.success(request, "Success ! Profile did not change . Please update your information to make a change")
            if first_name != "" or last_name != "" or email != "":
                profile = Account.objects.filter(pk=request.user.pk).update(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                )

                messages.info(
                    request, "Success !! Profile information updated successfully !!"
                )
            return redirect("profile")


class WishlistView(ListView):
    model = frontend_wishlist
    ordering = ["-created_at"]
    template_name: str = "frontend/account/wishlist.html"
    context_object_name = "wishlist"

    def post(self, request, *args, **kwargs):
        if "user_account_add_to_cart" in request.POST:
            wishlist_pk = request.POST.get("wishlistpk")
            # fetch wishlist data from wishlist model
            wishlist_object = wishlist.objects.filter(
                pk=wishlist_pk, user=request.user
            ).first()
            # seach in cart is this book is already in cart
            book_cart = cart.objects.filter(
                product_id=wishlist_object.product_id, user=request.user
            )
            if book_cart.exists():
                messages.error(request, "This book is already in your cart ")
                return redirect("wishlist")
            # add cart new record
            cart.objects.create(user=request.user, **cart_format(wishlist_object))
            wishlist_object.delete()

            messages.success(
                request, f"{wishlist_object.booktitle} added to cart successfully !"
            )
            return redirect("wishlist")


def cart_format(book):
    return {
        "product_id": str(book.product_id),
        "booktitle": book.booktitle,
        "bookquantity": 1,
        "bookthumbnail": book.bookthumbnail,
        "bookprice": float(book.bookprice),
        "booktype": book.booktype,
        "bookauthor": book.bookauthor,
        "bookslug": book.bookslug,
    }
