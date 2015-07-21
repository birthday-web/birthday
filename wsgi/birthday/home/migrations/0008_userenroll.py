# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20150713_1512'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserEnroll',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(unique=True, max_length=254)),
                ('username', models.CharField(unique=True, max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('date_of_birth', models.DateField(verbose_name=b'Date of Birth')),
                ('image', models.ImageField(upload_to=b'images/user_enroll/%Y/%m/%d')),
            ],
        ),
    ]
