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

    url('^accounts/', include('django.contrib.auth.urls')),
    # url('^accounts/login/$', auth_views.login, name='login'),
    url('^accounts/signup/$', view.signup),
    url('^index/$', view.index_ignore, name='index'),


    # personal page url, including customers' and artists'
    url('^personal_world/(?P<customer_id>[0-9]+)/$', personal_controller.personal_art_world, name='personal_world')

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

