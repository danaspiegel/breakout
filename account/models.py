from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from thumbs import ImageWithThumbsField

import lifestream.models

# short_name is a user's first name and last initial
User.short_name = property(lambda self: "%s %s." % (self.first_name, self.last_name[0:1]))
User.get_absolute_url = models.permalink(lambda self: ('account_view', (), { 'username': self.username, }))

DEFAULT_PROFILE_IMAGE_PATH = 'profile_images/default_breakout_profile_image.png'

class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    profile_image = ImageWithThumbsField(max_length=400, upload_to='profile_images', sizes=((48, 48), (64, 64), (200, 200)), default=ImageWithThumbsField(DEFAULT_PROFILE_IMAGE_PATH))
    age = models.PositiveSmallIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    occupation = models.CharField(max_length=100, blank=True, null=True)
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