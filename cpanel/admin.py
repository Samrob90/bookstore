from django.contrib import admin
from . import models

# Register your models here.

# register_products
class product(admin.ModelAdmin):
    model = models.product
    list_display = ("product_name", "product_type", "created_at")


admin.site.register(models.product, product)


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


# register userliked
class register_User_likes(admin.ModelAdmin):
    model = models.UserLikes
    list_display = ("user", "ratings", "liked", "disliked")


admin.site.register(models.UserLikes, register_User_likes)


class register_rating(admin.ModelAdmin):
    model = models.ratings
    list_display = (
        "user",
        "stars",
        "title",
        "comments",
        "likes",
        "dislikes",
        "created_at",
    )


admin.site.register(models.ratings, register_rating)


class register_address(admin.ModelAdmin):
    model = models.Addresse
    list_display = (
        "user",
        "user_type",
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
    list_display = (
        "orderid",
        "email",
        "status",
        "payment_method",
        "amount",
        "created_at",
    )


admin.site.register(models.order, register_orders)


# deal of week
class register_deal_of_week(admin.ModelAdmin):
    model: models.DealofWeek
    list_display = (
        "book",
        "discount",
        "periode",
        "quantity",
        "sold",
        "created_at",
    )


admin.site.register(models.DealofWeek, register_deal_of_week)


# register author
class register_author(admin.ModelAdmin):
    model: models.Authors
    list_display = ("fullname", "nofp", "description", "created_at")


admin.site.register(models.Authors, register_author)
