import os.path

from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
import django.contrib.auth.views

from django.contrib import admin
admin.autodiscover()

from feeds import feeds
from breakout.models import VenueSitemap

urlpatterns = patterns('',
    url(r'^', include('breakout.urls')),
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^oauth/twitter/', include('twitter_app.urls')),
    url(r'^accounts/', include('account.urls')),

    url(r'^contact/', include('contact_form.urls')),    
    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    url(r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', { 'sitemaps': { 'venues': VenueSitemap() } }),
    url(r'^robots.txt$', include('django_robots.urls')),
    # url(r"^announcements/", include('django_announcements.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(.*)$', 'django.views.static.serve', kwargs={'document_root': os.path.join(settings.PROJECT_PATH, 'media')}),
    	url(r'^storage/(?P<path>.*)$','django.views.static.serve',kwargs={'document_root': os.path.join(settings.PROJECT_PATH,'storage')}),
    )
