# Generated by Django 4.1.7 on 2023-05-09 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0006_alter_listing_active"),
    ]

    operations = [
        migrations.AlterField(
            model_name="listing",
            name="active",
            field=models.CharField(default="active", max_length=64),
        ),
    ]