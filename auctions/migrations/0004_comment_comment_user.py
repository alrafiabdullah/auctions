# Generated by Django 3.0.8 on 2020-07-14 08:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_watchlist_watcher'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='comment_user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
