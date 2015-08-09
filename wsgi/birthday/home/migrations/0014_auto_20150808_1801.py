# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_auto_20150807_1826'),
    ]

    operations = [
        migrations.AddField(
            model_name='userenroll',
            name='reference_email',
            field=models.EmailField(default='zkhan1093@gmail.com', max_length=254),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='friendship',
            name='status',
            field=models.IntegerField(choices=[(1, b'Friend'), (2, b'Blocked'), (3, b'Requested')]),
        ),
    ]
