from django import template
from datetime import datetime, timezone

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
