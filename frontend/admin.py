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


class register_wishlist(admin.ModelAdmin):
    model = models.wishlist
    list_display = ("product_id", "booktitle", "booktype", "bookauthor", "created_at")


admin.site.register(models.wishlist, register_wishlist)
