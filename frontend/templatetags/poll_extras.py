from django import template
from datetime import datetime, date
from django.utils import timezone
from dateutil import parser
from pandas import to_datetime as pd_datetime
from cpanel.models import order, order_book, book

register = template.Library()


@register.filter(name="get_range")
def get_range(value):
    return range(1, int(value))


@register.filter(name="total_")
def get_total(qty, value):
    return float(qty) * float(value)


@register.filter(name="addbyone")
def addone(value):
    return int(value) + 1


@register.filter(name="filter_rating")
def filter_rating(obj, stars):
    return obj.filter(stars=stars).count()


@register.filter(name="stars_perentage")
def stars_perentage(stars, totalreview):
    try:
        return int((int(stars) * 100) / int(totalreview))
    except ZeroDivisionError:
        return 0


@register.filter(name="available_book_deal")
def available_book_deal(sold, quantity):
    return quantity - sold


@register.filter(name="deal_of_the_weak_percentage")
def deal_of_the_weak_percentage(price, percentage):
    return int(float(price) - (float(price) * float(percentage) / 100))


@register.filter(name="check_expiration")
def check_expiration(timestamp):
    now = datetime.now(timezone.utc)
    if now > timestamp:
        return "expired"
    else:
        try:
            return str(timestamp - now).split(".")[0]
        except:
            return timestamp - now


@register.filter(name="get_order_qty")
def get_order_qty(obj):
    qty = 0
    for i in obj:
        qty += int(i.bookquantity)
    return qty


@register.filter(name="substration")
def substration(val, obj):
    return float(val) - float(obj)


@register.filter(name="new_expiration")
def new_expiration(timestamp):
    now = datetime.now(timezone.utc)
    return pd_datetime(timestamp) > now
    # return timestamp < now
    # val = datetime.strptime(str(timestamp)[:10], "%Y-%m-%d %H:%M:%S")
    # aware = timezone("UTC").localize(datetime.now())
    # return timestamp < now


@register.filter(name="string_to_dic")
def string_to_dic(string):
    array = string.split(";")
    bookdetails = []
    for i in array:
        second = i.split("***")
        if len(second) > 1:
            if second[0] != "" and second[1] != "":
                bookdetails.append([second[0].replace("_", " "), second[1]])
    return bookdetails


@register.filter(name="check_order_complete")
def check_order_complete(bookid):
    order_obj = order.objects.filter(status="delivered", order_book__product_id=bookid)
    print(order_obj)
    if order_obj.exists:
        return True
