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
# from django.contrib import admin


from ArtGallery.Controller import views_complaints
from . import view
import xadmin
from xadmin.plugins import xversion

xadmin.autodiscover()
xversion.register_models()

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^$', view.hello),
    url('^accounts/', include('django.contrib.auth.urls')),
    url('^accounts/signup/$', view.signup),
    # complaints need 4 urls, the art_info is fake one
    url('^art_info/complaints/(?P<artwork_id>[0-9]+)$', views_complaints.edit_complaints, name='edit_complaints'),
    url('^art_info/complaints_withdraw/(?P<artwork_id>[0-9]+)$', views_complaints.withdraw_complaints,
        name='withdraw_complaints'),

    url('^art_info/$', views_complaints.art_info),
    url('^art_info/complaints/action/$', views_complaints.complaints_action, name='complaints_action'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

