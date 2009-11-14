import os.path

from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
import django.contrib.auth.views

from django.contrib import admin
admin.autodiscover()

from contact_form.forms import AkismetContactForm
from feeds import feeds
from breakout.models import VenueSitemap, BreakoutSessionSitemap

sitemaps = {
    'venues': VenueSitemap,
    'breakout_sessions': BreakoutSessionSitemap,
}

urlpatterns = patterns('',
    url(r'^', include('breakout.urls')),
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^oauth/twitter/', include('twitter_app.urls')),
    url(r'^accounts/', include('account.urls')),

    url(r'^contact/$', 'contact_form.views.contact_form', { 'form_class': AkismetContactForm }, name='contact_form'),
    url(r'^contact/sent/$', direct_to_template, { 'template': 'contact_form/contact_form_sent.html' }, name='contact_form_sent'),
    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    url(r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', { 'sitemaps': sitemaps }),
    url(r'^robots.txt', 'django_robots.urls.rules_list', name='robots_rule_list'),
    # url(r"^announcements/", include('django_announcements.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(.*)$', 'django.views.static.serve', kwargs={'document_root': os.path.join(settings.PROJECT_PATH, 'media')}),
    	url(r'^storage/(?P<path>.*)$','django.views.static.serve',kwargs={'document_root': os.path.join(settings.PROJECT_PATH, 'storage')}),
    )
