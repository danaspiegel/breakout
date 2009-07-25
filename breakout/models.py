import datetime

from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import *
from django.core.urlresolvers import reverse
from django.contrib.sitemaps import Sitemap
from django.contrib.localflavor.us.models import USStateField, PhoneNumberField


class Venue(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(name='Short Name', unique=True)
    description = models.TextField(null=True, blank=True)
    street_address_1 = models.CharField(max_length=100)
    street_address_2 = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100)
    state = USStateField()
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    url = models.URLField(max_length=400, verify_exists=False, blank=True, null=True)
    image = models.ImageField(max_length=400, upload_to='venues', blank=True, null=True)
        
    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        return ('venue_view', (), { 'venue_slug': self.slug })
    
    @property
    def past_breakout_sessions(self):
        today = datetime.datetime.now()
        return self.breakout_sessions.filter(end_date__lt=datetime.datetime(today.year, today.month, today.day)).order_by('-start_date')
    
    @property
    def future_breakout_sessions(self):
        today = datetime.datetime.now()
        return self.breakout_sessions.filter(start_date__gt=datetime.datetime(today.year, today.month, today.day)).order_by('start_date')
    
    @property
    def current_breakout_session(self):
        try:
            today = datetime.datetime.now()
            return self.breakout_sessions.get(end_date__gte=today, start_date__lte=today)
        except BreakoutSession.DoesNotExist:
            return None
    
    @property
    def next_breakout_session(self):
        try:
            return self.future_breakout_sessions[0]
        except BreakoutSession.DoesNotExist:
            return None
    
    class Meta:
        get_latest_by = 'updated_on'

class BreakoutCategory(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=50)    
    slug = models.SlugField(name='Short Name', unique=True)
    description = models.TextField(null=True, blank=True)
    order = models.PositiveSmallIntegerField(default=20, choices=((i, str(i)) for i in range(1, 40)))
    
    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        return ('session_list', (), { 'category_slug': self.slug })
    
    class Meta:
        get_latest_by = 'updated_on'
        ordering = ['order', ]
        verbose_name = 'Breakout Category'
        verbose_name_plural = 'Breakout Categories'


class BreakoutSession(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(BreakoutCategory, related_name='breakout_sessions')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    moderator = models.ForeignKey(User, related_name='moderating_sessions')
    registered_users = models.ManyToManyField(User, related_name='registered_sessions', through='SessionAttendance')
    venue = models.ForeignKey(Venue, related_name='breakout_sessions')
    available_spots = models.PositiveSmallIntegerField(null=True, blank=True)
    
    def __unicode__(self):
        return '%s at %s' % (self.name, self.venue, )
    
    @models.permalink
    def get_absolute_url(self):
        return ('session_view', (), { 'session_id': self.id, 'venue_slug': self.venue.slug })
    
    def is_active(self):
        return self.start_date <= datetime.datetime.now() <= self.end_date
    
    class Meta:
        get_latest_by = 'updated_on'
        verbose_name = 'Breakout Session'
        verbose_name_plural = 'Breakout Sessions'


class SessionAttendance(models.Model):
    STATUS_CHOICES = (
        ('R', 'Registered'),
        ('P', 'Participating'),
        ('A', 'Attended'),
    )
    registrant = models.ForeignKey(User, related_name='session_attendance')
    session = models.ForeignKey(BreakoutSession, related_name='session_attendance')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='R')
    arrival_time = models.DateTimeField(null=True, blank=True)
    departure_time = models.DateTimeField(null=True, blank=True)
    
    def __unicode__(self):
        return '%s %s %s' % (self.registrant, self.get_status_display(), self.session.name, )
    
    class Meta:
        get_latest_by = 'updated_on'
        verbose_name = 'Session Attendance'
        verbose_name_plural = 'Session Attendance'

# Sitemap class for django.contrib.sitemaps
class VenueSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5

    def items(self):
        return Venue.objects.all().order_by('-created_on')

    def lastmod(self, obj):
        return obj.statuses.latest().created_on
