# Generated by Django 3.0.8 on 2020-07-15 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_auto_20200715_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='winnerlist',
            name='latest_bid',
            field=models.FloatField(),
        ),
    ]
