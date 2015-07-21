# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_auto_20150713_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='friend',
            name='email',
            field=models.EmailField(default=2, max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='friend',
            name='name',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
