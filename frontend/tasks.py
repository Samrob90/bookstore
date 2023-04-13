from celery import shared_task

# from . import models
from authentications.models import Account
from cpanel.models import book, order, Addresse, order_book, coupon
from authentications.models import Account

# from cpanel import models
from frontend.models import recent_viewied_item, cart
from rsc.SendMail import sendSelf

# import random
# import string


# send message from contact us form to support@newtonbookshop.com


@shared_task
def send_to_support(data):
    sendSelf(data=data)
    return "done"


@shared_task
def save_recent(pk, data):
    # check if user id is not not (not auhtenticated)
    if pk is not None:
        user = getUser(pk)
        book_exist_in_recent_view = recent_viewied_item.objects.filter(
            user=user, product_id=data["product_id"]
        )
        if book_exist_in_recent_view.exists():
            book_exist_in_recent_view.delete()
        else:
            recent_viewied_item.objects.create(user=user, **data)
    return "done"


@shared_task
def check_recent_view(data, userpk):
    user = getUser(userpk)
    for index, value in enumerate(data):
        product_db_id = recent_viewied_item.objects.filter(
            user=user, product_id=value["product_id"]
        )
        if product_db_id.exists():
            continue
        else:
            recent_viewied_item.objects.create(user=user, **value)

    return "done"


def getUser(userpk):
    try:
        return Account.objects.get(pk=userpk)
    except KeyError:
        return None


def db_format(user, data):
    new_dict = {"user": user}
    return new_dict.update(data)


@shared_task
def save_order(data):
    user = Account.objects.filter(email=data["email"])
    address = None
    coupon_obj = None

    # check if coupon is not emtpty
    if data["coupon"] is not None:
        obj = coupon.objects.filter(code=data["coupon"])
        if obj.exists():
            coupon_obj = obj.first()

    if data["address_type"] == "user_select_address":
        address = Addresse.objects.filter(pk=data["addressid"]).first()
    elif data["address_type"] == "user_new_address":
        # creare address
        address = save_address(data["address"], "user")
    else:
        address = save_address(data["address"], "guest")

    new_order = order.objects.create(
        orderid=data["orderid"],
        email=data["email"],
        # items=data["items"],
        address=address,
        coupon=coupon_obj,
        amount=data["total"],
        payment_method=data["payment_method"],
        shipping_fee=data["shipping_fee"],
        discount=data["discount"],
    )

    for i in data["items"]:
        del i["user"]
        order_book.objects.create(ordernumber=new_order, **i)

    if user.exists():
        cart.objects.filter(user=user.first()).delete()
    else:
        pass  # delete cookie from brownser

    send_mail_after_save(data["email"], data["items"])
    return "done"


def send_mail_after_save(email, items):
    pass


def save_address(data, user_type):
    return Addresse.objects.create(
        user=data["email"],
        user_type=user_type,
        first_name=data["first_name"],
        last_name=data["last_name"],
        address1=data["address1"],
        address2=data["address2"],
        country=data["country"],
        region_or_state=data["state"],
        city=data["city"],
        phonenumber=data["number"],
    )


# @shared_task
# def save_order(data):
#     user = Account.objects.filter(email=data["email"])
#     address = 0

#     if data["address_type"] == "user_select_address":
#         address = Addresse.objects.filter(pk=data["addressid"]).first()
#     elif data["address_type"] == "user_new_address":
#         # creare address
#         address = save_address(data["address"], "user")
#     else:
#         address = save_address(data["address"], "guest")

#     order.objects.create(
#         orderid=data["orderid"],
#         email=data["email"],
#         items=data["items"],
#         address=address,
#         payment_method=data["payment_method"],
#     )

#     if user.exists():
#         cart.objects.filter(user=user.first()).delete()
#     else:
#         pass  # delete cookie from brownser

#     send_mail_after_save(data["email"], data["items"])
#     return "done"
