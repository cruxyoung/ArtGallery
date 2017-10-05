# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-07 02:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ArtWork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aw_name', models.CharField(max_length=64, null=True)),
                ('aw_img', models.ImageField(default='/static/images/profile-default.png', upload_to='')),
                ('aw_description', models.CharField(max_length=256, null=True)),
                ('aw_location', models.CharField(max_length=32, null=True)),
                ('aw_time', models.DateTimeField()),
                ('aw_type', models.CharField(max_length=32, null=True)),
                ('aw_genre', models.CharField(max_length=32, null=True)),
                ('aw_auctionStat', models.BooleanField()),
                ('aw_totalAward', models.FloatField(default=0.0)),
                ('artist_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AuctionHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ah_amount', models.FloatField(default=0.0)),
                ('ah_aucTime', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='AuctionRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ar_originalPrice', models.FloatField(default=0.0)),
                ('ar_time', models.DateTimeField()),
                ('ar_finalPrice', models.FloatField(null=True)),
                ('aw_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ArtGallery.ArtWork')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_content', models.CharField(max_length=256, null=True)),
                ('comment_time', models.DateTimeField()),
                ('rating', models.FloatField(default=5.0)),
                ('replay_commentId', models.IntegerField(null=True)),
                ('aw_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ArtGallery.ArtWork')),
                ('commenter_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('complaint_type', models.CharField(default='Illegal', max_length=32)),
                ('complaint_content', models.CharField(max_length=256, null=True)),
                ('complaint_time', models.DateTimeField()),
                ('aw_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ArtGallery.ArtWork')),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FavoriteRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fav_time', models.DateTimeField()),
                ('artist_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('aw_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ArtGallery.ArtWork')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender_id', models.IntegerField()),
                ('receiver_id', models.IntegerField()),
                ('notifyType', models.CharField(max_length=32, null=True)),
                ('aw_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ArtGallery.ArtWork')),
            ],
        ),
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reward_amount', models.FloatField(default=0.0)),
                ('reward_time', models.DateTimeField()),
                ('aw_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ArtGallery.ArtWork')),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=16)),
                ('sex', models.BooleanField()),
                ('birthday', models.DateTimeField(null=True)),
                ('amount', models.FloatField(default=0.0)),
                ('identity', models.BooleanField()),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='auctionhistory',
            name='ar_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ArtGallery.AuctionRecord'),
        ),
        migrations.AddField(
            model_name='auctionhistory',
            name='customer_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
