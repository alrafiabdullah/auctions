# Generated by Django 3.0.8 on 2020-07-15 12:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_auto_20200715_1833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='bid_count',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='bid',
            name='bid_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='bid',
            name='of_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.AuctionListing'),
        ),
    ]
