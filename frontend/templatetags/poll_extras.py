from django import template

register = template.Library()


@register.filter(name="get_range")
def get_range(value):
    return range(value)


@register.filter(name="total_")
def get_total(qty, value):
    return float(qty) * float(value)
