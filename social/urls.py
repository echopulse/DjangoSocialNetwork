from django.conf.urls import patterns, url, include
from social import views
from social.models import Message
#from rest_framework import obtain_auth_token

urlpatterns = patterns('',
    # main page
    url(r'^$', views.index),
    # signup page
    url(r'^signup/$', views.signup),
    # register new user
    url(r'^register/$', views.register),
    # login page
    url(r'^login/$', views.login),
    # logout page
    url(r'^logout/$', views.logout),
    # members page
    url(r'^members/$', views.members),
    # friends page
    url(r'^friends/$', views.friends),
    # user profile edit page
    url(r'^profile/$', views.profile),
    # Ajax: check if user exists
    url(r'^checkuser/$', views.checkuser),
    # messages page
    url(r'^messages/(?P<view_user>\w+)$', views.messages),
    #API link
    #url(r'^api/token/', obtain_auth_token, name='api-token'),
)
