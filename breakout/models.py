import datetime
from geopy import geocoders

from django.conf import settings
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
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    
    geocoder = geocoders.Google(settings.GOOGLE_MAPS_API_KEY)
    
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
    def recent_past_breakout_sessions(self):
        today = datetime.datetime.now()
        return self.breakout_sessions.filter(end_date__lt=datetime.datetime(today.year, today.month, today.day)).order_by('-start_date')[0:5]
    
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
            return self.future_breakout_sessions[0:1]
        except BreakoutSession.DoesNotExist:
            return None
    
    def geocode(self):
        place, (self.latitude, self.longitude) = Venue.geocoder.geocode("%s, %s, %s %s" % (self.street_address_1, self.city, self.state, self.zip_code, ))
        return place
    
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
        return ('upcoming_session_list', (), { 'category_slug': self.slug })
    
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
    
    @property
    def event_date(self):
        return self.start_date.date()
    
    @property
    def remaining_spots(self):
        if self.available_spots:
            return self.available_spots - self.registered_users.count()
        else:
            return None
    
    @property
    def attending_users(self):
        return self.registered_users.filter(session_attendance__status='A')
    
    @models.permalink
    def get_absolute_url(self):
        return ('session_view', (), { 'session_id': self.id, 'venue_slug': self.venue.slug })
    
    def is_active(self):
        return self.start_date <= datetime.datetime.now() <= self.end_date
    is_active.boolean = True
    
    """
    Returns a list of all of the different lifestream objects ordered by created_on
    """
    @property
    def lifestream(self):
        pass
        
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
    
    def length(self):
        return self.departure_time - self.arrival_time
    
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
