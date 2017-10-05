# -*- coding:utf8 -*-

import xadmin

from .models import UserProfile, ArtWork, AuctionRecord, AuctionHistory, Reward, FavoriteRecord, Complaint, Comment
from xadmin import views


# add themes changing for management system
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


# change the title, footer name. And customize the menu
class GlobalSettings(object):
    site_title = 'ArtGallery Management System'
    site_footer = 'Art Gallery Online Platform'
    menu_style = 'accordion'


# create the classes for every table of ArtGallery
class UserProfileAdmin(object):
    list_display = ['user_id', 'password', 'sex', 'birthday', 'amount', 'identity']
    search_fields = ['user_id', 'password', 'sex', 'birthday', 'amount', 'identity']
    list_filter = ['user_id', 'password', 'sex', 'birthday', 'amount', 'identity']


class ArtWorkAdmin(object):
    list_display = ['artist_id', 'aw_name', 'aw_description', 'aw_location', 'aw_time', 'aw_type', 'aw_genre']
    # list_display = ['aw_totalAward']
    search_fields = ['artist_id', 'aw_name', 'aw_location', 'aw_type', 'aw_genre']
    list_filter = ['artist_id', 'aw_name', 'aw_location', 'aw_time', 'aw_type', 'aw_genre', 'aw_totalAward']


class AuctionRecordAdmin(object):
    list_display = ['aw_id', 'ar_originalPrice', 'ar_time', 'ar_finalPrice']
    search_fields = ['aw_id', 'ar_originalPrice', 'ar_finalPrice']
    list_filter = ['aw_id', 'ar_originalPrice', 'ar_time', 'ar_finalPrice']


class AuctionHistoryAdmin(object):
    list_display = ['ar_id', 'customer_id', 'ah_amount', 'ah_aucTime']
    search_fields = ['ar_id', 'customer_id', 'ah_amount']
    list_filter = ['ar_id', 'customer_id', 'ah_amount', 'ah_aucTime']


class RewardAdmin(object):
    list_display = ['customer_id', 'aw_id', 'reward_amount', 'reward_time']
    search_fields = ['customer_id', 'aw_id', 'reward_amount']
    list_filter = ['customer_id', 'aw_id', 'reward_amount', 'reward_time']


class FavoriteRecordAdmin(object):
    list_display = ['artist_id', 'aw_id', 'fav_time']
    search_fields = ['artist_id', 'aw_id']
    list_filter = ['artist_id', 'aw_id', 'fav_time']


class ComplaintAdmin(object):
    list_display = ['aw_id', 'customer_id', 'complaint_type', 'complaint_time']
    search_fields = ['aw_id', 'customer_id', 'complaint_type']
    list_filter = ['aw_id', 'customer_id', 'complaint_type', 'complaint_time']


class CommentAdmin(object):
    list_display = ['commenter_id', 'aw_id', 'comment_content', 'comment_time', 'rating']
    search_fields = ['commenter_id', 'aw_id', 'comment_content', 'rating']


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)

xadmin.site.register(UserProfile, UserProfileAdmin)
xadmin.site.register(ArtWork, ArtWorkAdmin)
xadmin.site.register(AuctionRecord, AuctionRecordAdmin)
xadmin.site.register(AuctionHistory, AuctionHistoryAdmin)
xadmin.site.register(Reward, RewardAdmin)
xadmin.site.register(FavoriteRecord, FavoriteRecordAdmin)
xadmin.site.register(Complaint, ComplaintAdmin)
xadmin.site.register(Comment, CommentAdmin)
