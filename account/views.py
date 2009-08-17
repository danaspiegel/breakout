import httplib, time, datetime

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.encoding import smart_unicode, force_unicode
import django.contrib.auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site, RequestSite

import twitter_app.utils
import twitter_app.oauth
import simplejson

from models import *
from forms import *

CONSUMER = twitter_app.oauth.OAuthConsumer(twitter_app.utils.CONSUMER_KEY, twitter_app.utils.CONSUMER_SECRET)
CONNECTION = httplib.HTTPSConnection(twitter_app.utils.SERVER)

# def login(request):
#     redirect_to = request.REQUEST.get('next', '')
#     if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
#         redirect_to = settings.LOGIN_REDIRECT_URL
#     if request.user.is_authenticated():
#         return HttpResponseRedirect(reverse('profile', kwargs={ 'screen_name': request.user.get_profile().twitter_user.screen_name }))
#     return render_to_response('account/login.html', {}, context_instance=RequestContext(request))

def twitter_login(request):
    request_token = twitter_app.utils.get_unauthorised_request_token(CONSUMER, CONNECTION)
    auth_url = twitter_app.utils.get_authorisation_url(CONSUMER, request_token)
    response = HttpResponseRedirect(auth_url)
    request.session['twitter_oauth_request_token'] = request_token.to_string()   
    return response

def logout(request):
    django.contrib.auth.logout(request)
    return HttpResponseRedirect(reverse('index'))

def twitter_callback(request):
    twitter_oauth_request_token = request.session.get('twitter_oauth_request_token', None)
    if not twitter_oauth_request_token:
        # request.user.message_set.add("There was an issue generating login information for Twitter OAuth. Please try to login again.")
        return HttpResponseRedirect(reverse('index'))
    request_token = twitter_app.utils.oauth.OAuthToken.from_string(twitter_oauth_request_token)   
    if request_token.key != request.GET.get('oauth_token', 'no-token'):
        # request.user.message_set.add("There was an authentication error with Twitter OAuth. Please try to login again.")
        return HttpResponseRedirect(reverse('index'))
    # use the access token to log the user in
    try:
        user = django.contrib.auth.authenticate(request_token=request_token)
        if user:
            if user.is_active:
                django.contrib.auth.login(request, user)
                return HttpResponseRedirect(reverse('profile', kwargs={ 'screen_name': user.get_profile().twitter_user.screen_name }))
            else:
                request.user.message_set.add("Your FrHire account has been disabled. Please contact support if you have any questions.")
    except:
        pass
        # request.user.message_set.add("There was an authentication error with Twitter OAuth. Please try to login again.")
    return HttpResponseRedirect(reverse('index'))

# This was taken from django-registration (partly, anyway)
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect(reverse('configure_services', kwargs={ 'user_id': user.id }))
    else:
        form = RegistrationForm()
    return render_to_response('registration/registration_form.html', { 'form': form }, context_instance=RequestContext(request))

def configure_services(request, user_id):
    pass


def password_reset(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            opts = { 'use_https': request.is_secure(), 'token_generator': default_token_generator, }
            form.save(**opts)
            return HttpResponseRedirect(reverse('password_reset_done'))
    else:
        form = PasswordResetForm()
    return render_to_response('account/password_reset_form.html', { 'form': form, }, context_instance=RequestContext(request))

