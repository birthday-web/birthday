# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import home.models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_userenroll'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friend',
            name='image',
            field=models.ImageField(upload_to=home.models.get_friend_image_path),
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(upload_to=home.models.get_post_image_path),
        ),
        migrations.AlterField(
            model_name='userenroll',
            name='image',
            field=models.ImageField(upload_to=home.models.get_enroll_image_path),
        ),
    ]
