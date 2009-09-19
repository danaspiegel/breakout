from django.conf.urls.defaults import *

from views import venue, breakout_session

urlpatterns = patterns('',
    url(r'^$', breakout_session.index, name='index'),
    url(r'^venues/$', venue.list, name='venue_list'),
    url(r'^venues/(?P<venue_slug>[\w\-\_]+)/$', venue.view, name='venue_view'),
    url(r'^venues/(?P<venue_slug>[\w\-\_]+)/sessions/$', breakout_session.list, name='breakout_session_list'),
    url(r'^venues/(?P<venue_slug>[\w\-\_]+)/upcoming/$', breakout_session.list, kwargs={ 'include_past': False }, name='upcoming_breakout_session_list'),
    url(r'^venues/(?P<venue_slug>[\w\-\_]+)/archive/$', venue.archive, name='archive_breakout_session_list'),
    url(r'^venues/(?P<venue_slug>[\w\-\_]+)/(?P<breakout_session_id>[\w\-\_]+)/$', breakout_session.view, name='breakout_session_view'),
    url(r'^venues/(?P<venue_slug>[\w\-\_]+)/(?P<breakout_session_id>[\w\-\_]+)/register/$', breakout_session.register, name='breakout_session_register'),
    url(r'^venues/(?P<venue_slug>[\w\-\_]+)/(?P<breakout_session_id>[\w\-\_]+)/unregister/$', breakout_session.unregister, name='breakout_session_unregister'),
    url(r'^venues/(?P<venue_slug>[\w\-\_]+)/(?P<breakout_session_id>[\w\-\_]+)/checkin/$', breakout_session.checkin, name='breakout_session_checkin'),
    url(r'^venues/(?P<venue_slug>[\w\-\_]+)/(?P<breakout_session_id>[\w\-\_]+)/checkout/$', breakout_session.checkout, name='breakout_session_checkout'),
    url(r'^sessions/$', breakout_session.list, name='breakout_session_list'),
    url(r'^sessions/create/$', breakout_session.create, name='breakout_session_create'),
    url(r'^sessions/upcoming/$', breakout_session.list, kwargs={ 'include_past': False }, name='breakout_session_list'),
    url(r'^sessions/past/$', breakout_session.list, kwargs={ 'include_future': False }, name='past_breakout_session_list'),
    url(r'^sessions/(?P<session_format_slug>[\w\-\_]+)/$', breakout_session.list, name='breakout_session_list'),
    url(r'^sessions/(?P<session_format_slug>[\w\-\_]+)/upcoming/$', breakout_session.list, kwargs={ 'include_past': False }, name='upcoming_breakout_session_list'),
    url(r'^sessions/(?P<session_format_slug>[\w\-\_]+)/past/$', breakout_session.list, kwargs={ 'include_future': False }, name='past_breakout_session_list'),
    
    url(r'^ical/sessions/$', breakout_session.ical, name='breakout_session_list_ical'),
    
)
