from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
    url(r'login/$', views.login, name='login'),
    url(r'^login/twitter/$', views.twitter_login, name='twitter_login'),
    url(r'logout/$', views.logout, name='logout'),
    url(r'^oauth/twitter/callback/$', views.twitter_callback, name='twitter_callback'),
)
