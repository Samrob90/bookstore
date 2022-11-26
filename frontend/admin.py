from django.contrib import admin
from . import models

# Register your models here.


class ShoppingCart(admin.ModelAdmin):
    model = models.cart
    list_display = (
        "product_id",
        "booktitle",
        "bookquantity",
        "booktype",
        "bookauthor",
        "created_at",
    )


admin.site.register(models.cart, ShoppingCart)
