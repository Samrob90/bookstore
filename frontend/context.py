from django.template.context_processors import request
from authentications import forms
from functools import reduce
from frontend.models import cart as frontend_cart
from django.db.models import Sum
from frontend import models
from cpanel.models import general_settings

# from . import models


def user_context(request):
    general_content = dict()
    value = []
    categorie = models.category.objects.all()

    if request.user.is_authenticated:
        total_price = 0
        value = frontend_cart.objects.filter(user=request.user).order_by("-created_at")
        if value is not None:
            for i in value:
                total_price += float(i.bookprice) * float(i.bookquantity)
        get_cart(general_content, value, total_price)
    else:
        if "cart" in request.session:
            result = grabe_children(request.session["cart"])
            get_cart(general_content, result[0], result[1])
        else:
            general_content["cart_total"] = 0

        general_content["login_form"] = forms.LoginForm()

    general_content["categories"] = categorie
    general_content["general_settings"] = general_settings.objects.all().first()
    return general_content


def get_cart(general_content, cart_data, total_):
    general_content["cart"] = cart_data
    general_content["cart_total"] = len(cart_data)
    general_content["cart_price_total"] = total_
    general_content["cart_type"] = type


def grabe_children(item):
    local_list = []
    localtotal = 0
    for item_id in item:
        for items in item[item_id]:
            local_list.append(items)
            localtotal += float(items["bookprice"]) * float(items["bookquantity"])

    return [local_list, localtotal]
