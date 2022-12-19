from django.contrib import admin
from . import models

# Register your models here.


class books(admin.ModelAdmin):
    model = models.book
    list_display = (
        "title",
        "quantity",
        "author",
        "review",
        "default_price",
        "default_type",
        "thumbnail",
        "created_at",
    )


admin.site.register(models.book, books)


class bookimage(admin.ModelAdmin):
    model = models.bookimages
    list_display = ("book", "thumbnail", "images", "created_at")


admin.site.register(models.bookimages, bookimage)


# book detials register
class bookdetail(admin.ModelAdmin):
    model = models.bookdetails
    list_display = ("book", "booktype", "price", "description")


admin.site.register(models.bookdetails, bookdetail)


class register_general_setting(admin.ModelAdmin):
    model = models.general_settings
    list_display = (
        "site_title",
        "tage_line",
        "default_email",
        "default_phone",
        # "facebook_handle",
        # "twitter_handle",
        # "instagram_handle",
        # "youtube_handle",
        "pinterest_handle",
        "address",
    )


admin.site.register(models.general_settings, register_general_setting)


class register_rating(admin.ModelAdmin):
    model = models.rating
    list_display = ("stars", "comment", "likes", "dislikes", "created_at")


admin.site.register(models.rating, register_rating)


class register_address(admin.ModelAdmin):
    model = models.Addresse
    list_display = (
        "user",
        "address1",
        "country",
        "region_or_state",
        "city",
    )


admin.site.register(models.Addresse, register_address)


class register_coupon(admin.ModelAdmin):
    model = models.coupon
    list_display = ("created_by", "code", "expires_on", "percentage", "created_at")


admin.site.register(models.coupon, register_coupon)


class register_orders(admin.ModelAdmin):
    model = models.order
    list_display = ("orderid", "email", "status", "payment_method", "created_at")


admin.site.register(models.order, register_orders)
