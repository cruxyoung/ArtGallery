# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-08 08:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ArtGallery', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='complaint_time',
            field=models.DateTimeField(null=True),
        ),
    ]
