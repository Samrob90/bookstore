from django.db import models
import uuid
from django.utils import timezone
from django.urls import reverse
from authentications.models import Account
from django.db.models import Avg
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

# import jsonfield
# from django.utils.translation import gettext_lazy as _

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
    slug = models.SlugField(default=None, unique=True)
    default_price = models.DecimalField(decimal_places=2, max_digits=9)
    default_type = models.CharField(
        choices=bookchoice, default=PAPERBACK, max_length=250
    )
    description = models.TextField(default=None)
    thumbnail = models.CharField(max_length=250, default=None)
    category = models.CharField(max_length=300, default=None)
    created_at = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse(
            "book-detail",
            kwargs={
                "uuid": self.product.product_id,
                "slug": self.slug,
            },
        )

    # get avarage ratuings
    def avarage_ratings(self) -> float:
        avr_ratings = ratings.objects.filter(book=self).aggregate(Avg("stars"))[
            "stars__avg"
        ] or float(0)
        return float(str(avr_ratings)[:3])

    def __str__(self) -> str:
        return self.title


# book ratings
class ratings(models.Model):
    user = models.ForeignKey(
        Account, verbose_name="user rating", on_delete=models.CASCADE
    )
    book = models.ForeignKey(
        "book", verbose_name="book rated", on_delete=models.CASCADE
    )
    stars = models.IntegerField(default=0)
    title = models.TextField(default=None)
    comments = models.TextField(default=None, blank=True, null=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    # def aravage_ratings(self) -> float:
    #     return self.fi

    def __str__(self) -> str:
        return f"{self.book.title} : {self.book.avarage_ratings()}"


class UserLikes(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    ratings = models.ForeignKey(
        ratings, verbose_name="user likes", on_delete=models.CASCADE
    )
    liked = models.BooleanField(default=False)
    disliked = models.BooleanField(default=False)
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
    description = models.TextField(default=None, null=True, blank=True)
    # using string for detials detials instead jsonField because qslite does not support JsonField
    # there is other alternative but i find this easier and simple . Convert data to string separeted by ';' then split it by comment when it
    details = models.TextField(default="None", null=True, blank=True)

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
    user = models.EmailField(default=None)
    user_type = models.CharField(max_length=30, default="guest")
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
    order_number = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    orderid = models.CharField(
        default="None",
        max_length=10,
    )
    email = models.EmailField(default=None)
    status = models.CharField(max_length=250, default="pending")
    address = models.ForeignKey(
        "Addresse", verbose_name="shipping address", on_delete=models.CASCADE
    )
    coupon = models.ForeignKey(
        "coupon",
        verbose_name="coupon code",
        on_delete=models.CASCADE,
        default=None,
        null=True,
        blank=True,
    )
    # coupon = models.CharField(max_length=250, default=None, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=None)
    payment_method = models.CharField(default=None, max_length=250)
    shipping_fee = models.CharField(default=None, max_length=250)
    discount = models.CharField(default=None, max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.orderid

    def get_absolute_url(self):
        return reverse("cpanel_order_detials", kwargs={"pk": self.pk})


class order_book(models.Model):
    ordernumber = models.ForeignKey(
        "order", verbose_name="cart", on_delete=models.CASCADE
    )
    product_id = models.CharField(max_length=150, default=None)
    booktitle = models.CharField(max_length=250, default=None)
    bookquantity = models.IntegerField(default=None)
    bookthumbnail = models.CharField(max_length=250, default=None)
    bookprice = models.DecimalField(decimal_places=2, max_digits=9)
    booktype = models.CharField(max_length=250, default=None)
    bookauthor = models.CharField(max_length=250, default=None)
    bookslug = models.CharField(max_length=250, default=None, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.booktitle


class OnSale(models.Model):
    book = models.ForeignKey(
        "book", verbose_name="book on sale", on_delete=models.CASCADE
    )
    discount = models.IntegerField(default=None, verbose_name="discount (%)")
    periode = models.DateTimeField(default=None)
    created_at = models.DateTimeField(default=timezone.now)


class DealofWeek(models.Model):
    book = models.ForeignKey(
        "book", verbose_name="Choose a book", on_delete=models.CASCADE
    )
    discount = models.IntegerField(default=None, verbose_name="Discount off (%)")
    periode = models.DateTimeField(default=None, verbose_name="Expirind date")
    quantity = models.IntegerField(default=None, verbose_name="Books quantity")
    sold = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{book.title}"


class Authors(models.Model):
    books = models.ManyToManyField(
        book, verbose_name="author book", default=None, blank=True
    )
    fullname = models.CharField(default=None, max_length=300)
    nofp = models.IntegerField(default=None, verbose_name="number of books published")
    description = models.TextField(default=None)
    thumbnail = models.ImageField(
        upload_to="author/thumbnail", default="author_defualt_thumbnail.webp"
    )
    image = models.ImageField(
        upload_to="author/img", default="None", null=True, blank=True
    )
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, **kwargs):
        output_size = (445, 300)
        output_thumb = BytesIO()
        img = Image.open(self.image)
        img_name = self.image.name.split(".")[0]

        # if img.height >445 or img.width > 445:
        img.thumbnail(output_size)
        img.save(output_thumb, format="WEBP", quality=90)
        self.thumbnail = InMemoryUploadedFile(
            output_thumb,
            "ImageField",
            f"{img_name}_thumb.webp",
            "image/webp",
            sys.getsizeof(output_thumb),
            None,
        )

        super(Authors, self).save()

    def get_absolute_url(self):
        return reverse("author_single", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return self.fullname
