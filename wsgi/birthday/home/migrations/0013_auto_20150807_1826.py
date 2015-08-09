# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_auto_20150731_1101'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friendship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.IntegerField(choices=[(1, b'Friend'), (2, b'Blocked')])),
            ],
        ),
        migrations.AlterField(
            model_name='friend',
            name='quote',
            field=models.CharField(max_length=500, blank=True),
        ),
        migrations.AddField(
            model_name='friendship',
            name='from_person',
            field=models.ForeignKey(related_name='from_friend', to='home.Friend'),
        ),
        migrations.AddField(
            model_name='friendship',
            name='to_person',
            field=models.ForeignKey(related_name='to_friend', to='home.Friend'),
        ),
        migrations.AddField(
            model_name='friend',
            name='friends',
            field=models.ManyToManyField(related_name='friend_with+', through='home.Friendship', to='home.Friend'),
        ),
    ]
