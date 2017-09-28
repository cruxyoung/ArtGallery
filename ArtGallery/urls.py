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
from django.contrib import admin
from . import views
from . import ajax

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.hello),
    url('^accounts/', include('django.contrib.auth.urls')),
    url('^accounts/signup/$', views.signup),
    url('^accounts/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^artwork/(?P<aw_id>[0-9]+)/detail/$', views.artwork_detail, name='aw'),
    url(r'^artist/(?P<user_id>[0-9]+)/detail/$', views.artist_detail, name='user'),
    url(r'^auction/(?P<auction_id>[0-9]+)/detail/$', views.auction_detail, name='auction'),
    url(r'^artwork/(?P<aw_id>[0-9]+)/reward/$', views.reward_pay, name='reward'),
    url(r'^artwork/(?P<aw_id>[0-9]+)/detail/comment/$', views.ajax_comment, name='comment'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.ARTWORK_URL, document_root=settings.ARTWORK_ROOT)
