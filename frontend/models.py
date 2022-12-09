from django.db import models
import uuid
from django.utils import timezone
from authentications.models import Account
from django_cleanhtmlfield.fields import HTMLField

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

    def __str__(self):
        return self.subcategory


class recent_viewied_item(models.Model):
    user = models.ForeignKey(Account, verbose_name="cart", on_delete=models.CASCADE)
    product_id = models.CharField(max_length=150, default=None)
    booktitle = models.CharField(max_length=250, default=None)
    bookquantity = models.IntegerField(default=1, null=True, blank=True)
    bookthumbnail = models.CharField(max_length=250, default=None)
    bookprice = models.DecimalField(decimal_places=2, max_digits=9)
    booktype = models.CharField(max_length=250, default=None)
    bookauthor = models.CharField(max_length=250, default=None)
    bookslug = models.CharField(max_length=250, default=None, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)


class faq(models.Model):
    question = models.TextField(default=None)
    answer = models.TextField(default=None)
    created_at = models.TextField(default=timezone.now)


class about_us(models.Model):
    start = HTMLField(strip_unsafe=True, widget_form_class=True)
    our_story = HTMLField(strip_unsafe=True, widget_form_class=True)
    our_who = HTMLField(strip_unsafe=True, widget_form_class=True)
    our_why = HTMLField(strip_unsafe=True, widget_form_class=True)
    our_what = HTMLField(strip_unsafe=True, widget_form_class=True)
    our_where = HTMLField(strip_unsafe=True, widget_form_class=True)
    our_when = HTMLField(strip_unsafe=True, widget_form_class=True)
    our_how = HTMLField(strip_unsafe=True, widget_form_class=True)
    our_price = HTMLField(strip_unsafe=True, widget_form_class=True)
    our_philosophy = HTMLField(strip_unsafe=True, widget_form_class=True)
    our_mantra = HTMLField(strip_unsafe=True, widget_form_class=True)
    our_goal = HTMLField(strip_unsafe=True, widget_form_class=True)
    who_we_serve = HTMLField(strip_unsafe=True, widget_form_class=True)

    def __str__(self) -> str:
        return self.start
