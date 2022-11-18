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
