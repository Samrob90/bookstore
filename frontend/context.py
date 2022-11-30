from django.template.context_processors import request
from authentications import forms
from functools import reduce
from frontend.models import cart as frontend_cart
from django.db.models import Sum

# from . import models


def user_context(request):
    cart = dict()
    value = []

    if request.user.is_authenticated:
        total_price = 0
        value = frontend_cart.objects.filter(user=request.user)
        if value is not None:
            for i in value:
                total_price += float(i.bookprice)
        get_cart(cart, value, total_price, "db")

        return cart

    elif "cart" in request.session:
        result = grabe_children(request.session["cart"])
        get_cart(cart, result[0], result[1], "session")
        cart["login_form"] = forms.LoginForm()
        return cart
    else:
        cart["login_form"] = forms.LoginForm()
        cart["cart_total"] = 0
        return cart


def get_cart(cart, cart_data, total_, type):
    cart["cart"] = cart_data
    cart["cart_total"] = len(cart_data)
    cart["cart_price_total"] = total_
    cart["cart_type"] = type


def grabe_children(item):
    local_list = []
    localtotal = 0
    for item_id in item:
        for items in item[item_id]:
            local_list.append(items)
            localtotal += float(items["book_price"]) * float(items["book_quantity"])

    return [local_list, localtotal]
