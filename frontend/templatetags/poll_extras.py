from django import template

register = template.Library()


@register.filter(name="get_range")
def get_range(value):
    return range(1, int(value))


@register.filter(name="total_")
def get_total(qty, value):
    return float(qty) * float(value)


@register.filter(name="addbyone")
def addone(value):
    print(value)
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
    return float(price) - (float(price) * float(percentage) / 100)
