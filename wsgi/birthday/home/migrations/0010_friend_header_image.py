# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_auto_20150730_2306'),
    ]

    operations = [
        migrations.AddField(
            model_name='friend',
            name='header_image',
            field=models.ImageField(default='', upload_to=b'friends/headers'),
            preserve_default=False,
        ),
    ]
