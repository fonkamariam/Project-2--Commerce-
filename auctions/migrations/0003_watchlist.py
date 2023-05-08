# Generated by Django 4.1.7 on 2023-05-08 13:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0002_listing"),
    ]

    operations = [
        migrations.CreateModel(
            name="Watchlist",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "oneauction",
                    models.ManyToManyField(
                        blank=True,
                        null=True,
                        related_name="oneauction",
                        to="auctions.listing",
                    ),
                ),
                (
                    "own",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="userWL",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]