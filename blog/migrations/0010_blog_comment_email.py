# Generated by Django 4.1.3 on 2022-12-09 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0009_remove_blog_comment_commented_by_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="blog_comment",
            name="email",
            field=models.CharField(default=None, max_length=300),
        ),
    ]