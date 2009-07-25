from django.conf.urls.defaults import *

from views import venue, session

urlpatterns = patterns('',
    url(r'^$', session.list, kwargs={ 'include_past': False }, name='index'),
    url(r'^venues/$', venue.list, name='venue_list'),
    url(r'^venues/(?P<venue_slug>[\w\-\_]+)/$', venue.view, name='venue_view'),
    url(r'^venues/(?P<venue_slug>[\w\-\_]+)/sessions/$', session.list, name='session_list'),
    url(r'^venues/(?P<venue_slug>[\w\-\_]+)/upcoming/$', session.list, kwargs={ 'include_past': False }, name='upcoming_session_list'),
    url(r'^venues/(?P<venue_slug>[\w\-\_]+)/archive/$', session.list, kwargs={ 'include_future': False }, name='archive_session_list'),
    url(r'^venues/(?P<venue_slug>[\w\-\_]+)/(?P<session_id>[\w\-\_]+)/$', session.view, name='session_view'),
    url(r'^sessions/$', session.list, name='session_list'),
    url(r'^sessions/upcoming/$', session.list, kwargs={ 'include_past': False }, name='session_list'),
    url(r'^sessions/(?P<category_slug>[\w\-\_]+)/$', session.list, name='session_list'),
    url(r'^sessions/(?P<category_slug>[\w\-\_]+)/upcoming/$', session.list, kwargs={ 'include_past': False }, name='upcoming_session_list'),
)
