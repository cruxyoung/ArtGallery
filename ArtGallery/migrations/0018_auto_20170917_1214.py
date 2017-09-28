# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-17 12:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ArtGallery', '0017_auto_20170915_1100'),
    ]

    operations = [
        migrations.RenameField(
            model_name='favoriterecord',
            old_name='artist_id',
            new_name='customer_id',
        ),
        migrations.AlterField(
            model_name='artwork',
            name='aw_img',
            field=models.ImageField(default='/static/images/profile-default.png', upload_to='artwork/1505650472.076344'),
        ),
    ]