# Generated by Django 3.0.8 on 2020-07-15 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_auto_20200715_1830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='bid_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
