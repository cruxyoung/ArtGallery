from django.db import models
from django.contrib.auth.models import User
import time


# User profile, represent table "user" in design
# Inherit THE DJANGO EMBEDDED AUTHENICATION SYSTEM
# THE EMBEDDED SYSTEM ALREADY INCLUDE NAME AND EMAIL

class UserProfile(models.Model):
    user_id = models.ForeignKey(User, verbose_name='User Name')

    password = models.CharField(max_length=16, verbose_name='Password')
    sex = models.BooleanField(verbose_name='Gender')
    birthday = models.DateTimeField(null=True, verbose_name='Birthday')
    amount = models.FloatField(default=0.0, verbose_name='Amount')
    identity = models.BooleanField(verbose_name='Identity')


# Artwork
class ArtWork(models.Model):
    # Foreign Key
    artist_id = models.ForeignKey(User, verbose_name='Artist Name')

    aw_name = models.CharField(null=True, max_length=64, verbose_name='Artwork Name')
    aw_img = models.ImageField(default="/static/images/profile-default.png",
                               upload_to='artwork/' + time.time().__str__(),
                               verbose_name='Image')
    # aw_img = models.ImageField(default="/static/images/profile-default.png", verbose_name='Image')
    aw_description = models.CharField(null=True, max_length=256, verbose_name='Description')
    aw_location = models.CharField(null=True, max_length=32, verbose_name='Location')
    aw_time = models.DateTimeField(verbose_name='Add Time')
    aw_type = models.CharField(null=True, max_length=32, verbose_name='Type')
    aw_genre = models.CharField(null=True, max_length=32, verbose_name='Genre')
    aw_auctionStat = models.BooleanField(verbose_name='Auction Status')
    aw_totalAward = models.FloatField(default=0.0, verbose_name='Total Award')

    # class Meta:
    #     verbose_name = 'Artwork'
    #     verbose_name_plural = verbose_name

    def __str__(self):
        return self.aw_name


class AuctionRecord(models.Model):
    # Foreign Key
    aw_id = models.ForeignKey(ArtWork, verbose_name='Artwork Name')

    ar_originalPrice = models.FloatField(default=0.0, verbose_name='Original Price')
    ar_time = models.DateTimeField(verbose_name='Auction Time')
    ar_finalPrice = models.FloatField(null=True, verbose_name='Final Price')

    ar_period = models.FloatField(null=True, verbose_name='Period')

    def __str__(self):
        return str(self._get_pk_val())


# Auction History
class AuctionHistory(models.Model):
    # Foreign Key
    ar_id = models.ForeignKey(AuctionRecord, verbose_name='Auction Record ID')
    customer_id = models.ForeignKey(User, verbose_name='Customer')

    ah_amount = models.FloatField(default=0.0, verbose_name='Auction Amount')
    ah_aucTime = models.DateTimeField(verbose_name='Auction Time')


# Reward
class Reward(models.Model):
    # Foreign Key
    customer_id = models.ForeignKey(User, verbose_name='Customer')
    aw_id = models.ForeignKey(ArtWork, verbose_name='Artwork Name')

    reward_amount = models.FloatField(default=0.0, verbose_name='Reward Amount')
    reward_time = models.DateTimeField(verbose_name='Reward Time')


# Favorite Record
class FavoriteRecord(models.Model):
    # Foreign Key

    artist_id = models.ForeignKey(User, verbose_name='Artist Name')
    aw_id = models.ForeignKey(ArtWork, verbose_name='Artwork Name')

    fav_time = models.DateTimeField(verbose_name='Favourite Time')


# Complaint and Comment
class Complaint(models.Model):
    # Foreign Key
    aw_id = models.ForeignKey(ArtWork, verbose_name='Artwork Name')
    customer_id = models.ForeignKey(User, verbose_name='Customer')

    complaint_type = models.CharField(default='Illegal', max_length=32, verbose_name='Complaint Type')
    complaint_content = models.CharField(null=True, max_length=256, verbose_name='Complaint Content')
    complaint_time = models.DateTimeField(null=True, verbose_name='Complaint Time')


class Comment(models.Model):
    # Foreign Key
    # commenter could be artist or customer
    commenter_id = models.ForeignKey(User, verbose_name='Commenter Name')
    aw_id = models.ForeignKey(ArtWork, verbose_name='Artwork Name')

    comment_content = models.CharField(null=True, max_length=256, verbose_name='Comment Content')
    comment_time = models.DateTimeField(verbose_name='Comment Time')
    rating = models.FloatField(default=5.0, verbose_name='Rating')
    reply_commentId = models.IntegerField(null=True)
