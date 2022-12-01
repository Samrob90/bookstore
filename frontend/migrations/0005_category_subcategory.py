# Generated by Django 4.1.3 on 2022-12-01 11:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("frontend", "0004_wishlist"),
    ]

    operations = [
        migrations.CreateModel(
            name="category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("category", models.CharField(default=None, max_length=250)),
                ("tag", models.CharField(default=None, max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name="subcategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("subcategory", models.CharField(default=None, max_length=150)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="frontend.category",
                        verbose_name="category",
                    ),
                ),
            ],
        ),
    ]