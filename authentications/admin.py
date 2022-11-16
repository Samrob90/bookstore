from django.contrib import admin
from . import models

# Register your models here.
class registerAccount(admin.ModelAdmin):
    model = models.Account
    list_display = (
        "email",
        "first_name",
        "last_name",
        "email_verify",
        "is_staff",
        "last_login",
        "date_joined",
    )


admin.site.register(models.Account, registerAccount)
