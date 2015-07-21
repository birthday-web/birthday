# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20150713_1040'),
    ]

    operations = [
        migrations.AddField(
            model_name='friend',
            name='image',
            field=models.ImageField(default=1, upload_to=b'images/%Y/%m/%d'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(upload_to=b'images/%Y/%m/%d'),
        ),
    ]
