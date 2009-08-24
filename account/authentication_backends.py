# Taken from http://www.djangosnippets.org/snippets/1473/

"""Twitter Authentication backend for Django

Requires:
AUTH_PROFILE_MODULE to be defined in settings.py

The profile models should have following fields:
        access_token
        url
        location
        description
        profile_image_url
"""

import httplib, time, datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.http import *

import simplejson

from twitter_app.utils import *

CONSUMER = oauth.OAuthConsumer(CONSUMER_KEY, CONSUMER_SECRET)
CONNECTION = httplib.HTTPSConnection(SERVER)

class TwitterBackend:
    """
    TwitterBackend for authentication
    """
    
    def authenticate(self, request_token):
        '''
        authenticates the token by requesting user information from twitter
        '''
        if not request_token:
            return None
        access_token = exchange_request_token_for_access_token(CONSUMER, CONNECTION, request_token)
        response_json = is_authenticated(CONSUMER, CONNECTION, access_token)
        auth = simplejson.loads(response_json)
        # from IPython import Shell; Shell.IPShellEmbed()()
        screen_name = auth['screen_name']
        twitter_id = auth['id']
        user, created = User.objects.get_or_create(username=screen_name)
        if created:
            # create and set a random password so user cannot login using django built-in authentication
            temp_password = User.objects.make_random_password(length=12)
            user.set_password(temp_password)
            # we need to set the user_profile.twitter_user
            user.get_profile().twitter_user, twitter_user_created = TwitterUser.objects.get_or_create(screen_name=screen_name, twitter_id=twitter_id)
            user.get_profile().save()
        user.first_name = auth.get('name').split(None, 1)[0] or ''
        user.last_name = auth.get('name').split(None, 1)[1] or ''
        user.save()
        
        # Get the user profile
        user_profile = user.get_profile()
        user_profile.twitter_access_token = oauth.OAuthToken.to_string(access_token)
        user_profile.twitter_user.url = auth['url']
        user_profile.twitter_user.profile_image_url = auth['profile_image_url']
        user_profile.twitter_user.location = auth['location']
        user_profile.twitter_user.description = auth['description']
        user_profile.twitter_user.save()
        user_profile.save()
        return user
    
    def get_user(self, id):
        try:
            return User.objects.get(pk=id)
        except:
            return None
