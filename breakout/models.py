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

from . import InactiveSessionException

import tagging
from tagging.fields import TagField

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
    
    tags = TagField()
    
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
            return self.future_breakout_sessions[0]
        except IndexError:
            return None
        
    
    def geocode(self):
        place, (self.latitude, self.longitude) = Venue.geocoder.geocode("%s, %s, %s %s" % (self.street_address_1, self.city, self.state, self.zip_code, ))
        return place
    
    class Meta:
        get_latest_by = 'updated_on'

tagging.register(Venue)

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
        return ('breakout_session_list', (), { 'category_slug': self.slug })
    
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
    # TODO: these fields must be made timezone aware
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
        return ('breakout_session_view', (), { 'breakout_session_id': self.id, 'venue_slug': self.venue.slug })
    
    @property
    def is_active(self):
        return self.start_date <= datetime.datetime.now() <= self.end_date
    
    @property
    def is_future(self):
        return self.start_date > datetime.datetime.now()
    
    @property
    def is_past(self):
        return not self.is_future and not self.is_active
    
    def is_registered(self, user):
        """
        Checks if a user is already registered to attend
        """
        return self.registered_users.filter(pk=user.pk).count() == 1

    def is_participating(self, user):
        """
        Checks if a user is already registered to attend
        """
        return self.registered_users.filter(pk=user.pk, session_attendance__status='P', session_attendance__departure_time=None).count() == 1
    
    @property
    def current_participants(self):
        """
        Returns a QuerySet of users that are currently participating in this Breakout Session
        """
        return self.registered_users.filter(session_attendance__status='P', session_attendance__departure_time=None)
    
    @property
    def participants(self):
        return self.registered_users.filter(session_attendance__status='P')
    
    def register(self, user):
        """
        Registers a user for a session
        * session must be in the future or currently happening
        """
        if self.is_active or self.is_future:
            session_attendance, created = SessionAttendance.objects.get_or_create(registrant=user, session=self)
            return created
        else:
            return False
    
    def unregister(self, user):
        """
        Un-registers a user for a session
        * session must be in the future or currently happening
        """
        if self.is_active or self.is_future:
            session_attendance = SessionAttendance.objects.get(registrant=user, session=self, status='R')
            session_attendance.delete()
            return True
        else:
            return False
    
    def checkin(self, user):
        """
        To be able to check into a breakout session:
        * session must exist
        * session must be active
        * user can only have a single registration, so if they have checked out, remove the checkout time
        
        >>> from datetime import datetime, timedelta
        >>> today = datetime.today()
        >>> start_date = datetime(year=today.year, month=today.month, day=today.day, hour=today.hour, minute=today.minute)
        >>> end_date = datetime(year=today.year, month=today.month, day=today.day, hour=today.hour + 1, minute=today.minute)
        >>> breakout_category = BreakoutCategory.objects.get(pk=1)
        >>> test_user_1, created = User.objects.get_or_create(username='test user 1')
        >>> test_user_2, created = User.objects.get_or_create(username='test user 2')
        >>> venue = Venue.objects.create(name="Test Venue", slug="test-venue", city="City", state="NY")
        >>> breakout_session, created = BreakoutSession.objects.get_or_create(name="Test Session", category=breakout_category, start_date=start_date, end_date=end_date, moderator=test_user_1, venue=venue)
        >>> breakout_session.is_active
        True
        >>> breakout_session.checkin(test_user_2)
        True
        >>> SessionAttendance.objects.filter(registrant=test_user_2, session=breakout_session).count()
        1
        
        # check that we only ever have a single entry per checked in user
        >>> breakout_session.checkin(test_user_2)
        True
        >>> SessionAttendance.objects.filter(registrant=test_user_2, session=breakout_session).count()
        1
        
        # check that the departure time is none
        >>> session_attendance = SessionAttendance.objects.get(registrant=test_user_2, session=breakout_session)
        >>> session_attendance.departure_time == None
        True
        >>> session_attendance.departure_time = datetime.today()
        >>> session_attendance.save()
        >>> breakout_session.checkin(test_user_2)
        True
        >>> session_attendance = SessionAttendance.objects.get(registrant=test_user_2, session=breakout_session)
        >>> session_attendance.departure_time == None
        True
        
        # check to make sure we throw an exception when session is inactive
        >>> start_date = datetime(year=today.year, month=today.month, day=today.day, hour=today.hour - 2, minute=today.minute)
        >>> end_date = datetime(year=today.year, month=today.month, day=today.day, hour=today.hour - 1, minute=today.minute)
        >>> inactive_breakout_session, created = BreakoutSession.objects.get_or_create(name="Test Session", category=breakout_category, start_date=start_date, end_date=end_date, moderator=test_user_1, venue=venue)
        >>> inactive_breakout_session.is_active
        False
        
        >>> inactive_breakout_session.checkin(test_user_2)
        Traceback (most recent call last):
        ...
        InactiveSessionException
        
        # check that we the right status set
        >>> session_attendance = SessionAttendance.objects.get(registrant=test_user_2, session=breakout_session)
        >>> session_attendance.get_status_display()
        u'Participated'
        
        >>> session_attendance.status = 'R'
        >>> session_attendance.save()
        >>> session_attendance.get_status_display()
        u'Registered'
        
        >>> breakout_session.checkin(test_user_2)        
        True
        >>> session_attendance = SessionAttendance.objects.get(registrant=test_user_2, session=breakout_session)
        >>> session_attendance.get_status_display()
        u'Participated'
        
        # check that we have the right arrival time (now if no prev. registration, old time if there was a previous registration)
        >>> SessionAttendance.objects.all().delete()
        >>> today = datetime.today()
        >>> breakout_session.checkin(test_user_2)        
        True
        >>> session_attendance = SessionAttendance.objects.get(registrant=test_user_2, session=breakout_session)
        >>> abs(session_attendance.arrival_time - today) < timedelta(seconds=5)
        True
        
        >>> session_attendance.arrival_time = breakout_session.start_date
        >>> session_attendance.save()
        >>> breakout_session.checkin(test_user_2)        
        True
        >>> session_attendance = SessionAttendance.objects.get(registrant=test_user_2, session=breakout_session)
        >>> session_attendance.arrival_time == breakout_session.start_date
        True
        """
        if not self.is_active:
            raise InactiveSessionException()
        session_attendance, created = SessionAttendance.objects.get_or_create(registrant=user, session=self)
        # if a user is checking in, then they are participating
        session_attendance.status = 'P'
        if not session_attendance.arrival_time:
            # if there is no arrival_time, set it now
            # if there was an arrival time, leave it alone
            session_attendance.arrival_time = datetime.datetime.now()
        # remove any departure time, since the user is now at the session
        session_attendance.departure_time = None
        session_attendance.save()
        return True
    
    def checkout(self, user):
        """
        To be able to check out of a breakout session:
        * session must exist
        * session must be active, or the checkout must be bound to the end of the session
        * user must have been checked in
        * user can only have a single registration, so if they have checked out, throw an exception, because you can't checkout twice
        """
        # raises a DoesNotExistException, which is correct
        session_attendance = SessionAttendance.objects.get(registrant=user, session=self)
        if session_attendance.status != 'P' or not session_attendance.arrival_time or session_attendance.departure_time:
            raise InvalidSessionCheckoutException()
        if self.end_date < datetime.datetime.now():
            session_attendance.departure_time = self.end_date
        else:
            session_attendance.departure_time = datetime.datetime.now()
        session_attendance.save()
        return True
        
    
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
        ('P', 'Participated'),
    )
    registrant = models.ForeignKey(User, related_name='session_attendance')
    session = models.ForeignKey(BreakoutSession, related_name='session_attendance')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='R')
    arrival_time = models.DateTimeField(null=True, blank=True)
    departure_time = models.DateTimeField(null=True, blank=True)
    
    def __unicode__(self):
        return '%s %s %s' % (self.registrant, self.get_status_display(), self.session.name, )
    
    def is_during(self, event_datetime):
        """
        Tests if the given event is happening between the arrival_time and departure time
        """
        if isinstance(event_datetime, datetime.datetime):
            return self.arrival_time <= event_datetime and (self.departure_time == None or self.departure_time >= event_datetime)
        return False
    
    def is_before(self, event_datetime):
        """
        Tests if the datetime is before the given event attendance
        """
        if isinstance(event_datetime, datetime.datetime):
            return self.arrival_time > event_datetime
        return False
    
    def is_after(self, event_datetime):
        """
        Tests if the datetime is after the given event attendance
        """
        if isinstance(event_datetime, datetime.datetime):
            return self.departure_time and self.departure_time < event_datetime
        return False
    
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
