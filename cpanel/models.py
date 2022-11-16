from django.db import models
import uuid
from django.utils import timezone

# Create your models here.
class product(models.Model):
    product_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    product_name = models.CharField(default=None, max_length=250)
    product_type = models.CharField(
        default=None, max_length=250, verbose_name="retial or wholesale"
    )
    created_at = models.DateTimeField(default=timezone.now)


class book(models.Model):
    PAPERBACK = "PAPERBACK"
    AUDIOBOOK = "AUDIOBOOK"
    EBOOK = "EBOOK"
    HARDCOVER = "HARDCOVER"
    bookchoice = (
        (PAPERBACK, "PAPERBACK"),
        (AUDIOBOOK, "AUDIOBOOK"),
        (EBOOK, "EBOOK"),
        (HARDCOVER, "HARDCOVER"),
    )

    product = models.ForeignKey(
        "product", verbose_name="product", on_delete=models.CASCADE
    )
    title = models.TextField(default=None)
    quantity = models.IntegerField(default=None)
    author = models.CharField(max_length=250, default=None, null=True, blank=True)
    review = models.IntegerField(default=None, null=True, blank=True)
    default_price = models.DecimalField(decimal_places=2, max_digits=9)
    deault_booktype = models.CharField(
        choices=bookchoice, default=PAPERBACK, max_length=250
    )
    thumbnail = models.CharField(max_length=250, default=None)
    created_at = models.DateTimeField(default=timezone.now)


class bookimages(models.Model):
    book = models.ForeignKey("book", verbose_name="book", on_delete=models.CASCADE)
    thumbnail = models.TextField(default=None, null=True, blank=True)
    images = models.ImageField(upload_to="media")
    created_at = models.DateTimeField(default=timezone.now)


class bookdetails(models.Model):
    book = models.ForeignKey("book", verbose_name="book", on_delete=models.CASCADE)
    booktype = models.CharField(max_length=150, default=None)
    price = models.DecimalField(decimal_places=2, max_digits=9)
    description = models.TextField(default=None)
