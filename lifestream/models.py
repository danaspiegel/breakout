import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

class LifestreamEntry(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name='lifestream_entries')
    breakout_session = models.ForeignKey('breakout.BreakoutSession', related_name='lifestream_entries')
    
    def __unicode__(self):
        return "%s @ %s" % (self.user.short_name, self.breakout_session.name, )
    
    class Meta:
        verbose_name = 'Lifestream Entry'
        verbose_name_plural = 'Lifestream Entries'
        ordering = ['-created_on', ]
        get_latest_by = 'updated_on'

class TwitterUser(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    twitter_id = models.PositiveIntegerField(unique=True)
    screen_name = models.CharField(max_length=50, unique=True)
    url = models.URLField(max_length=400, verify_exists=False, blank=True, null=True)
    profile_image_url = models.URLField(max_length=400, verify_exists=False)
    location = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    is_muted = models.BooleanField(default=False)
    
    def __unicode__(self):
        return "@%s" % self.screen_name
    
    def get_absolute_url(self):
        return 'http://twitter.com/%s' % self.screen_name
    
    def _tweet_count(self):
        return self.statuses.count()
    tweet_count = property(_tweet_count)
    
    def update_from_twitter(self, user_details):
        self.twitter_id = user_details.get('id')
        self.url = user_details.get('url')
        self.profile_image_url = user_details.get('profile_image_url')
        self.location = user_details.get('location')
        self.description = user_details.get('description')
    
    class Meta:
        verbose_name = 'Twitter User'
        verbose_name_plural = 'Twitter Users'
        get_latest_by = 'updated_on'

class TwitterStatus(LifestreamEntry):
    twitter_id = models.PositiveIntegerField()
    twitter_user = models.ForeignKey(TwitterUser, related_name='twitter_statuses')
    text = models.CharField(max_length=250)
    location = models.CharField(max_length=100, blank=True, null=True)
    
    def __unicode__(self):
        return "%s" % self.text
    
    class Meta:
        verbose_name = 'Twitter Status'
        verbose_name_plural = 'Twitter Statuses'

class FlickrImage(LifestreamEntry):
    url = models.URLField(max_length=400, verify_exists=False, blank=True, null=True)
