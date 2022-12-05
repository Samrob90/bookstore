from django.contrib import admin
from . import models

# Register your models here.
class register_blog(admin.ModelAdmin):
    model = models.blog
    list_display = ("blogid", "title", "likes", "views", "posted_by", "created_at")
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(models.blog, register_blog)


class register_blog_comment(admin.ModelAdmin):
    model = models.blog_comment
    list_display = ("blog", "comment", "commented_by", "created_at")


admin.site.register(models.blog_comment, register_blog_comment)
