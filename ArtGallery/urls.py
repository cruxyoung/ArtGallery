"""ArtGallery URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from .extra_apps import xadmin
from .extra_apps.xadmin.plugins import xversion

from ArtGallery.controllers import home_controller
from ArtGallery.controllers import views_complaints
from ArtGallery.controllers import account_controller
from ArtGallery.controllers import artwork_controller
from ArtGallery.controllers import personal_controller
from ArtGallery.controllers import artist_artworks_controller


xadmin.autodiscover()
xversion.register_models()

urlpatterns = [

    # Personal page url, including customers' and artists'
    url(r'^customer/favorites/$', personal_controller.PersonalFavorite.as_view(), name='favorite'),

    url(r'^customer/settings/$', personal_controller.PersonalSetting.as_view(), name='setting'),
    url(r'^customer/settings/change_pwd/$', personal_controller.PersonalSetting.as_view(), name='change_pwd'),
    url(r'^customer/settings/edit_info/$', personal_controller.UserInfoView.as_view(), name='edit_info'),

    url(r'^customer/complaints/$', personal_controller.PersonalComplaint.as_view(), name='complaint'),
    url(r'^customer/rewards/$', personal_controller.PersonalReward.as_view(), name='reward'),
    url(r'^customer/auctions/$', personal_controller.PersonalAuction.as_view(), name='auction'),
    url(r'^customer/comments/$', personal_controller.PersonalComment.as_view(), name='comment'),

    url(r'^artist/settings/$', artist_artworks_controller.ArtistSetting.as_view(), name='artist_setting'),
    url(r'^artist/artworks/$', artist_artworks_controller.ArtistArtwork.as_view(), name='artist_artwork'),
    url(r'^artist/artworks/edit/(?P<artwork_id>[0-9]+)/$', artist_artworks_controller.ArtworkEdit.as_view(),
        name='edit_artwork'),
    # auction history, existed when the artwork has auction record, which means the artwork open auction already
    url(r'^artist/artworks/edit/action/$', artist_artworks_controller.EditAction.as_view(), name='edit_action'),
    url(r'^artist/artworks/edit/auction/(?P<artwork_id>[0-9]+)/$', artist_artworks_controller.ArtworkAuction.as_view(),
        name='auctionSwitch'),
    url(r'^artist/artworks/auction_history/(?P<artwork_id>[0-9]+)/$',
        artist_artworks_controller.ArtworkAuction.as_view(), name='auctionHistory'),

    url(r'^artist/artworks/reward_history/(?P<artwork_id>[0-9]+)/$', artist_artworks_controller.ArtworkReward.as_view(),
        name='reward_history'),

    url(r'^artist/artworks/delete/(?P<artwork_id>[0-9]+)/$', artist_artworks_controller.delete_artwork,
        name='delete_artwork'),

    # Login and Logout
    url('^accounts/', include('django.contrib.auth.urls')),
    url('^accounts/signup/$', account_controller.signup, name='signup'),
    url('^accounts/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        account_controller.activate, name='activate'),

    # complaints need 4 urls, the art_info is fake one
    url('^art_info/complaints/(?P<artwork_id>[0-9]+)$', views_complaints.edit_complaints, name='edit_complaints'),
    url('^art_info/complaints_withdraw/(?P<artwork_id>[0-9]+)$', views_complaints.withdraw_complaints,
        name='withdraw_complaints'),

    url('^art_info/$', views_complaints.art_info),
    url('^art_info/complaints/action/$', views_complaints.complaints_action, name='complaints_action'),

    # Home Page and Information Page
    url('^index/', home_controller.home_page, name='index'),
    url(r'^(?P<art_id>[0-9]+)/$', home_controller.detail, name='detail'),
    url(r'^art_list/$', home_controller.art_list, name='art_list'),

    # Artwork Detail
    url(r'^artworks/(?P<aw_id>[0-9]+)/detail/$', artwork_controller.artwork_detail, name='aw'),
    url(r'^artwork/(?P<aw_id>[0-9]+)/detail/comment/$', artwork_controller.ajax_comment, name='comment'),
    url(r'^artwork/(?P<aw_id>[0-9]+)/detail/bid/$', artwork_controller.ajax_bid, name='bid'),
    url(r'^artwork/(?P<aw_id>[0-9]+)/reward/$', artwork_controller.ajax_reward, name='reward'),

    url(r'^artist/(?P<user_id>[0-9]+)/detail/$', artwork_controller.artist_detail, name='user'),

    url(r'^auction/(?P<auction_id>[0-9]+)/detail/$', artwork_controller.auction_detail, name='auction'),

    url(r'^xadmin/', xadmin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # urlpatterns += static(settings.ARTWORK_URL, document_root=settings.ARTWORK_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
