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


# register categry table
class r_category(admin.ModelAdmin):
    model = models.category
    list_display = ("category", "tag")


admin.site.register(models.category, r_category)

# register subcategory
class r_subcategory(admin.ModelAdmin):
    model = models.subcategory
    list_display = ("category", "subcategory")
    list_filter = ("category",)


admin.site.register(models.subcategory, r_subcategory)


# register recent_view class


class register_recent_view(admin.ModelAdmin):
    model = models.recent_viewied_item
    list_display = ("user", "product_id", "booktitle", "bookthumbnail")


admin.site.register(models.recent_viewied_item, register_recent_view)


class register_faq(admin.ModelAdmin):
    model = models.faq
    list_display = ("question", "answer", "created_at")


admin.site.register(models.faq, register_faq)


class register_about_us(admin.ModelAdmin):
    model = models.about_us
    list_display = ("start", "our_story", "our_who", "our_why")


admin.site.register(models.about_us, register_about_us)
