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
        "deault_booktype",
        "thumbnail",
        "created_at",
    )


admin.site.register(models.book, books)
