from django.conf.urls import patterns, url, include
from social import views

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'messages', views.MessageViewSet)
router.register(r'members', views.MemberViewSet)

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
    url(r'^api/', include(router.urls)),
)
