# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-14 13:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ArtGallery', '0004_auto_20170914_1315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artwork',
            name='aw_img',
            field=models.ImageField(default='/static/images/profile-default.png', upload_to='artwork/1505394957.287454'),
        ),
    ]
