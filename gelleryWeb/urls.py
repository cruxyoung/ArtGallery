from django.conf.urls import url

from.import views

# import gelleryWeb.views as gv

urlpatterns = {
    url(r'^index/$', views.index),
}