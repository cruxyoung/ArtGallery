from django.db import models
from django.contrib.auth.models import User
import time


# User profile, represent table "user" in design
# Inherit THE DJANGO EMBEDDED AUTHENICATION SYSTEM
# THE EMBEDDED SYSTEM ALREADY INCLUDE NAME AND EMAIL
class UserProfile(models.Model):
    user_id = models.ForeignKey(User)

    password = models.CharField(max_length=16)
    sex = models.BooleanField()
    birthday = models.DateTimeField(null=True)
    amount = models.FloatField(default=0.0)
    identity = models.BooleanField()


# Artwork
class ArtWork(models.Model):
    # Foreign Key
    artist_id = models.ForeignKey(User)

    aw_name = models.CharField(null=True, max_length=64)
    aw_img = models.ImageField(default="/static/images/profile-default.png", upload_to='artwork/'+time.time().__str__())
    aw_description = models.CharField(null=True, max_length=256)
    aw_location = models.CharField(null=True, max_length=32)
    aw_time = models.DateTimeField()
    aw_type = models.CharField(null=True, max_length=32)
    aw_genre = models.CharField(null=True, max_length=32)
    aw_auctionStat = models.BooleanField()
    aw_totalAward = models.FloatField(default=0.0)


# Auction Record
class AuctionRecord(models.Model):
    # Foreign Key
    aw_id = models.ForeignKey(ArtWork)

    ar_originalPrice = models.FloatField(default=0.0)
    ar_time = models.DateTimeField()
    ar_finalPrice = models.FloatField(null=True)


# Auction History
class AuctionHistory(models.Model):
    # Foreign Key
    ar_id = models.ForeignKey(AuctionRecord)
    customer_id = models.ForeignKey(User)

    ah_amount = models.FloatField(default=0.0)
    ah_aucTime = models.DateTimeField()


# Reward
class Reward(models.Model):
    # Foreign Key
    customer_id = models.ForeignKey(User)
    aw_id = models.ForeignKey(ArtWork)

    reward_amount = models.FloatField(default=0.0)
    reward_time = models.DateTimeField()


# Favorite Record
class FavoriteRecord(models.Model):
    # Foreign Key
    customer_id = models.ForeignKey(User)
    aw_id = models.ForeignKey(ArtWork)

    fav_time = models.DateTimeField()


# Complaint and Comment
class Complaint(models.Model):
    # Foreign Key
    aw_id = models.ForeignKey(ArtWork)
    customer_id = models.ForeignKey(User)

    complaint_type = models.CharField(default='Illegal', max_length=32)
    complaint_content = models.CharField(null=True, max_length=256)
    complaint_time = models.DateTimeField()


class Comment(models.Model):
    # Foreign Key
    # commenter could be artist or customer
    commenter_id = models.ForeignKey(User)
    aw_id = models.ForeignKey(ArtWork)

    comment_content = models.CharField(null=True, max_length=256)
    comment_time = models.DateTimeField()
    rating = models.FloatField(default=5.0)


# Notification
class Notification(models.Model):
    # Foreign Key
    aw_id = models.ForeignKey(ArtWork)

    sender_id = models.IntegerField()
    receiver_id = models.IntegerField()

    notifyType = models.CharField(null=True, max_length=32)

