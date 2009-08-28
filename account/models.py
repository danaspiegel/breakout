from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save

import lifestream.models

# short_name is a user's first name and last initial
User.short_name = property(lambda self: "%s %s." % (self.first_name, self.last_name[0:1]))

class UserProfile(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    twitter_access_token = models.CharField(max_length=500, blank=True, null=True)
    twitter_user = models.ForeignKey(lifestream.models.TwitterUser, related_name='twitter_user', blank=True, null=True)
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        ordering = ['-created_on', ]
        get_latest_by = 'updated_on'
    
    """
    Called when a user is saved to ensure that the user has a profile

    >>> user = User.objects.create(username='test', email='foo@bar.com')
    >>> user.get_profile()
    <UserProfile: test>
    """
    def __unicode__(self):
        return self.user.username


# Register a post save signal for BPUser to make sure that the profile is always created
def create_user_profile_callback(sender, instance, created, **kwargs):
    """
    Called when a user is saved to ensure that the user has a profile

    >>> user = User.objects.create(username='test', email='foo@bar.com')
    >>> user.get_profile()
    <UserProfile: test>

    Test that when the profile is deleted, it is recreated when the user is saved
    >>> UserProfile.objects.all().delete()
    >>> user = User.objects.get(username='test')
    >>> user.get_profile()
    Traceback (most recent call last):
    ...
    DoesNotExist: UserProfile matching query does not exist.

    >>> user.save()
    >>> user.get_profile()
    <UserProfile: test>

    >>> User.objects.all().delete()
    """
    try:
        instance.get_profile()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile_callback, sender=User)