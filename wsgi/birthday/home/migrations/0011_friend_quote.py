# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_friend_header_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='friend',
            name='quote',
            field=models.CharField(default='', max_length=500),
            preserve_default=False,
        ),
    ]
