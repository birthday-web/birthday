# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_friend_quote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friend',
            name='header_image',
            field=models.ImageField(upload_to=b'friends/headers', blank=True),
        ),
    ]
