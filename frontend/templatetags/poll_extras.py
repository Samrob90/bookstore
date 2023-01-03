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
