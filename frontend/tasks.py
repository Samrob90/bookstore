from celery import shared_task
from . import models
from authentications.models import Account
from cpanel.models import book, order
from frontend.models import recent_viewied_item, cart


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
            print(user.pk, value)
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
    user_email = data["email"]
    order.objects.create(**data)
    cart.objects.filter(user=user_email).delete()
    return "done"
