from django.db import models
import uuid
from django.utils import timezone
from django.urls import reverse
from authentications.models import Account


# Create your models here.
class product(models.Model):
    product_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    product_name = models.CharField(default=None, max_length=250)
    product_type = models.CharField(
        default=None, max_length=250, verbose_name="retial or wholesale"
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.product_name


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
    slug = models.SlugField(
        default=None,
    )
    default_price = models.DecimalField(decimal_places=2, max_digits=9)
    default_type = models.CharField(
        choices=bookchoice, default=PAPERBACK, max_length=250
    )
    thumbnail = models.CharField(max_length=250, default=None)
    created_at = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse(
            "book-detail",
            kwargs={
                "uuid": self.product.product_id,
                "slug": self.slug,
                "type": self.default_type,
            },
        )

    def __str__(self) -> str:
        return self.title


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
    # details = jsonfield.JSONField()
    def __str__(self):
        return self.book.title


class rating(models.Model):
    book = models.ForeignKey("book", verbose_name="book", on_delete=models.CASCADE)
    user = models.ForeignKey(Account, verbose_name="user", on_delete=models.CASCADE)
    stars = models.IntegerField(default=None)
    comment = models.TextField(default=None, null=True, blank=True)
    likes = models.IntegerField(default=0, null=True, blank=True)
    dislikes = models.IntegerField(default=0, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.book.title


class general_settings(models.Model):
    site_title = models.CharField(max_length=250, default=None)
    tage_line = models.CharField(
        max_length=250,
        default=None,
        help_text="In few words, explain what this site is about. ",
    )
    default_email = models.EmailField(
        default=None, help_text="The defaul email on home page."
    )
    default_phone = models.CharField(
        max_length=150, default=None, help_text="The default number on home page."
    )
    facebook_handle = models.CharField(
        max_length=150, default=None, help_text="Enter your facebook handle."
    )
    twitter_handle = models.CharField(
        max_length=150, default=None, help_text="Enter your twitter handle."
    )
    instagram_handle = models.CharField(
        max_length=150, default=None, help_text="Enter your intagram handle."
    )
    youtube_handle = models.CharField(
        max_length=150, default=None, help_text="Enter your youtube handle."
    )
    pinterest_handle = models.CharField(
        max_length=150, default=None, help_text="Enter your pinterest handle."
    )
    address = models.TextField(default=None, help_text="bookshop physical address")


class Addresse(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=300, default=None)
    last_name = models.CharField(max_length=300, default=None)
    address1 = models.CharField(max_length=300, default=None)
    address2 = models.CharField(max_length=300, default=None, null=True, blank=True)
    country = models.CharField(max_length=250, default=None)
    region_or_state = models.CharField(max_length=250, default=None)
    city = models.CharField(max_length=300, default=None)
    phonenumber = models.CharField(max_length=14, default=None, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.address1


class coupon(models.Model):
    created_by = models.ForeignKey(Account, on_delete=models.CASCADE)
    code = models.CharField(max_length=150, default=None)
    percentage = models.CharField(
        max_length=100, help_text="percentage ex: 20", default=None
    )
    expires_on = models.DateTimeField(default=None)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.code


class order(models.Model):
    orderid = models.UUIDField(uuid.uuid4, unique=True, editable=False)
    email = models.EmailField(default=None)
    status = models.CharField(max_length=250, default="pending")
    items = models.CharField(max_length=300, default=None)
    address = models.ForeignKey(
        "Addresse", verbose_name="shipping address", on_delete=models.CASCADE
    )
    payment_method = models.CharField(default=None, max_length=250)
    created_at = models.DateTimeField(default=timezone.now)
