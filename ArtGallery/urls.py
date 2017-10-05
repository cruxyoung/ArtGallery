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
from django.conf.urls import include
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin

from ArtGallery.controllers import account_controller
from ArtGallery.controllers import artwork_controller
from ArtGallery.controllers import personal_controller

from . import view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', view.hello),

    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/signup/$', view.signup),
    url(r'^index/$', view.index_ignore, name='index'),

    # personal page url, including customers' and artists'
    url(r'^customer/favorites/$', personal_controller.PersonalFavorite.as_view(), name='favorite'),

    url(r'^customer/settings/$', personal_controller.PersonalSetting.as_view(), name='setting'),
    url(r'^customer/settings/change_pwd/$', personal_controller.PersonalSetting.as_view(), name='change_pwd'),
    url(r'^customer/settings/edit_info/$', personal_controller.UserInfoView.as_view(), name='edit_info'),

    url(r'^customer/complaints/$', personal_controller.PersonalComplaint.as_view(), name='complaint'),
    url(r'^customer/rewards/$', personal_controller.PersonalReward.as_view(), name='reward'),
    url(r'^customer/auctions/$', personal_controller.PersonalAuction.as_view(), name='auction'),
    url(r'^customer/comments/$', personal_controller.PersonalComment.as_view(), name='comment'),

    url(r'^artist/settings/$', personal_controller.ArtistSetting.as_view(), name='artist_setting'),
    url(r'^artist/artworks/$', personal_controller.ArtistArtwork.as_view(), name='artist_artwork'),

    # Change Favorites
    # url(r'^customer/favorites/change_fav/$', ),

    # Login
    url('^accounts/', include('django.contrib.auth.urls')),
    url('^accounts/signup/$', account_controller.signup),

    url('^accounts/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        account_controller.activate, name='activate'),
    url(r'^artwork/(?P<aw_id>[0-9]+)/detail/$', artwork_controller.artwork_detail, name='aw'),
    url(r'^artwork/(?P<aw_id>[0-9]+)/detail/comment/$', artwork_controller.ajax_comment, name='comment'),
    url(r'^artist/(?P<user_id>[0-9]+)/detail/$', artwork_controller.artist_detail, name='user'),
    url(r'^auction/(?P<auction_id>[0-9]+)/detail/$', artwork_controller.auction_detail, name='auction'),
    url(r'^artwork/(?P<aw_id>[0-9]+)/reward/$', artwork_controller.reward_pay, name='reward'),
]

if settings.DEBUG:
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    urlpatterns += static(settings.ARTWORK_URL, document_root=settings.ARTWORK_ROOT)

