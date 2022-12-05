import sys
import uuid
from PIL import Image
from io import BytesIO
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django_cleanhtmlfield.fields import HTMLField
from django.core.files.uploadedfile import InMemoryUploadedFile

# Create your models here.
class blog(models.Model):
    blogid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    title = models.TextField(default=None)
    category = models.CharField(max_length=250, default=None, null=True, blank=True)
    article = HTMLField(strip_unsafe=True, widget_form_class=True)
    posted_by = models.CharField(max_length=250, default="Admin")
    likes = models.IntegerField(default=None)
    views = models.IntegerField(default=None)
    blogthumbnail = models.ImageField(
        upload_to="blog/thumbnail",
        null=None,
        blank=None,
        default="blog_thumbnail_default.webp",
    )
    blogimage = models.ImageField(upload_to="blog", default="blog_default.webp")
    slug = models.SlugField(default=None, null=False, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse("blog_detail", kwargs={"uuid": self.blogid, "slug": self.slug})

    def save(self, **kwargs):
        output_size = (445, 300)
        output_thumb = BytesIO()
        img = Image.open(self.blogimage)
        img_name = self.blogimage.name.split(".")[0]

        # if img.height >445 or img.width > 445:
        img.thumbnail(output_size)
        img.save(output_thumb, format="WEBP", quality=90)
        self.blogthumbnail = InMemoryUploadedFile(
            output_thumb,
            "ImageField",
            f"{img_name}_thumb.webp",
            "image/webp",
            sys.getsizeof(output_thumb),
            None,
        )

        super(blog, self).save()

    def __str__(self) -> str:
        return self.title


class blog_comment(models.Model):
    blog = models.ForeignKey(
        "blog", verbose_name="blog comments", on_delete=models.CASCADE
    )
    comment = models.TextField(default=None)
    commented_by = models.CharField(max_length=150, default=None)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.commented_by
