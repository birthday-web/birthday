# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0004_auto_20150713_1231'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friend',
            name='email',
        ),
        migrations.RemoveField(
            model_name='friend',
            name='name',
        ),
        migrations.AddField(
            model_name='friend',
            name='user',
            field=models.OneToOneField(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
