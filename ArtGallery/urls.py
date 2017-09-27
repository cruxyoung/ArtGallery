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
from django.conf.urls import url
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from ArtGallery import view
from ArtGallery.controllers import personal_controller
from django.contrib.auth import views as auth_views

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

    url(r'^customer/settings/test/$', personal_controller.TestHaha.as_view(), name='test_haha'),

    url(r'^customer/complaints/$', personal_controller.PersonalComplaint.as_view(), name='complaint'),
    url(r'^customer/rewards/$', personal_controller.PersonalReward.as_view(), name='reward'),
    url(r'^customer/auctions/$', personal_controller.PersonalAuction.as_view(), name='auction'),
    url(r'^customer/comments/$', personal_controller.PersonalComment.as_view(), name='comment'),

    # Change Favorites
    # url(r'^customer/favorites/change_fav/$', ),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
