# Generated by Django 4.1.3 on 2023-01-06 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cpanel", "0011_alter_order_coupon"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="coupon",
            field=models.CharField(blank=True, default=None, max_length=250, null=True),
        ),
    ]