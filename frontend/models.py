from django.db import models
import uuid
from django.utils import timezone
from authentications.models import Account

# Create your models here.
class cart(models.Model):
    user = models.ForeignKey(Account, verbose_name="cart", on_delete=models.CASCADE)
    product_id = models.CharField(max_length=150, default=None)
    booktitle = models.CharField(max_length=250, default=None)
    bookquantity = models.IntegerField(default=None)
    bookthumbnail = models.CharField(max_length=250, default=None)
    bookprice = models.DecimalField(decimal_places=2, max_digits=9)
    booktype = models.CharField(max_length=250, default=None)
    bookauthor = models.CharField(max_length=250, default=None)
    bookslug = models.CharField(max_length=250, default=None, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)


class wishlist(models.Model):
    user = models.ForeignKey(Account, verbose_name="cart", on_delete=models.CASCADE)
    product_id = models.CharField(max_length=150, default=None)
    booktitle = models.CharField(max_length=250, default=None)
    bookthumbnail = models.CharField(max_length=250, default=None)
    bookprice = models.DecimalField(decimal_places=2, max_digits=9)
    booktype = models.CharField(max_length=250, default=None)
    bookauthor = models.CharField(max_length=250, default=None)
    bookslug = models.CharField(max_length=250, default=None, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)


class category(models.Model):
    category = models.CharField(max_length=250, default=None)
    tag = models.CharField(max_length=250, default=None, null=True, blank=True)
    description = models.TextField(default=None, null=True, blank=True)

    def __str__(self):
        return self.category


class subcategory(models.Model):
    category = models.ForeignKey(
        "category", verbose_name="category", on_delete=models.CASCADE
    )
    subcategory = models.CharField(max_length=150, default=None)
