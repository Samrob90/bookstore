from urllib import request
from celery import shared_task
from rsc.SendMail import SendMail
from time import sleep
from urllib import request
from authentications import models
import time
from django.utils import timezone
from frontend import models as frontend_models


@shared_task()
def registration_verify_email(data, user_id=None):
    if user_id is not None:
        user = models.Account.objects.filter(pk=user_id).update(
            last_updated=timezone.now()
        )
    SendMail(data=data)
    return "done"


@shared_task
def check_cart(cart, pk):
    cart_in_session = grabe_children(cart)
    user = models.Account.objects.get(pk=pk)
    user_cart_value = frontend_models.cart.objects.filter(user=user)
    for cart_ in cart_in_session:
        if cart_["product_id"] in user_cart_value:
            continue
        else:
            frontend_models.cart.objects.create(
                user=user,
                product_id=cart_["product_id"],
                booktitle=cart_["book_title"],
                bookquantity=cart_["book_quantity"],
                bookthumbnail=cart_["book_thumbnail"],
                bookprice=cart_["book_price"],
                booktype=cart_["book_type"],
                bookauthor=cart_["book_author"],
                bookslug=cart_["book_slug"],
            )

    return "done"


def grabe_children(item):
    local_list = []
    for item_id in item:
        for items in item[item_id]:
            local_list.append(items)
    return local_list
