from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
import django.contrib.auth.views

import views

urlpatterns = patterns('',
    url(r'^login/$', django.contrib.auth.views.login, {'template_name': 'account/login.html'}, name='login'),
    url(r'^logout/$', django.contrib.auth.views.logout, {'template_name': 'account/logout.html'}, name='logout'),
    url(r'^password/change/$', django.contrib.auth.views.password_change, 
                                {'template_name': 'account/password_change_form.html'}, name='password_change'),
    url(r'^password/change/done/$', django.contrib.auth.views.password_change_done, 
                                {'template_name': 'account/password_change_done.html'}, name='password_change_done'),
    url(r'^password/reset/$', views.password_reset, name='password_reset'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', django.contrib.auth.views.password_reset_confirm, 
                                {'template_name': 'account/password_reset_confirm.html'}, name='password_reset_confirm'), 
    url(r'^password/reset/complete/$', django.contrib.auth.views.password_reset_complete, 
                                {'template_name': 'account/password_reset_complete.html'}, name='password_reset_complete'),
    url(r'^password/reset/done/$', django.contrib.auth.views.password_reset_done, 
                                {'template_name': 'account/password_reset_done.html'}, name='password_reset_done'),
    url(r'^register/$', views.register, name='registration_register'),
    url(r'^services/$', views.configure_services, name='configure_services'),
    url(r'^(?P<user_id>\w{3,})/services/$', views.configure_services, name='configure_services'),

    # url(r'^register/complete/$', direct_to_template, {'template': 'registration/registration_complete.html'}, name='registration_complete'),
    # url(r'^login/twitter/$', views.twitter_login, name='twitter_login'),
    # url(r'^oauth/twitter/callback/$', views.twitter_callback, name='twitter_callback'),
)
