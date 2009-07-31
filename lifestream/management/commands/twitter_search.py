"""
twitter_search.py

Here's the logic:

For all users that are logged in right now:
* get their TwitterUser (and thus name)
* if their TwitterUser account is not muted, get their statuses_user_timeline
* for all dates/times that they are "at" a BreakoutSession, capture the TwitterStatus

For all users that aren't logged in right now:
* for up to 1 week since event
* capture the TwitterStatus if it has the BreakoutSession hashtag

"""

import datetime
from dateutil.parser import parse
from django.core.management.base import CommandError, NoArgsCommand
from django.conf import settings

import pytwitter
import simplejson

from ...models import TwitterUser, TwitterStatus
import breakout.models

class Command(NoArgsCommand):    
    def handle_noargs(self, **options):
        imported_statuses = 0
        imported_users = 0
        api = pytwitter.pytwitter()
        search_api = pytwitter.pytwitter(url='http://search.twitter.com')
        
        # Get a list of all active sessions
        now = datetime.datetime.now()
        breakout_sessions = breakout.models.BreakoutSession.objects.filter(start_date__lte=now, end_date__gte=now)
        
        # for each active breakout session, iterate through the attending_users
        for breakout_session in breakout_sessions:
            print 'Looking at BreakoutSession: %s (%s)' % (breakout_session.name, breakout_session.id, )
            for user in breakout_session.attending_users:
                # if the user has a TwitterUser that's not muted
                twitter_user = user.get_profile().twitter_user
                if not twitter_user:
                    print '  User has no TwitterUser: %s' % (user.short_name, )
                    continue
                print '  Looking at User (screen_name): %s (%s)' % (user.short_name, twitter_user.screen_name, )                
                if not twitter_user.is_muted:
                    # get the paged twitter statuses
                    for page in xrange(1, 2):
                        # try:
                            response_json = api.statuses_user_timeline(screen_name=twitter_user.screen_name, page=page, rpp=100, format='json')
                            response = simplejson.loads(response_json)
                            if len(response) == 0: break
                            print '    Parsing page %s' % page
                            for result in response:
                                twitter_status, created = TwitterStatus.objects.get_or_create(twitter_id=result['id'], twitter_user=twitter_user, user=user, breakout_session=breakout_session)
                                if created:
                                    imported_statuses = imported_statuses + 1
                                    twitter_status.twitter_user = twitter_user
                                    twitter_status.text = result['text']
                                    twitter_status.created_on = parse(result['created_at'], ignoretz=True)
                                    twitter_status.location = twitter_user.location
                                    twitter_status.save()
                        # except Exception, e:
                            # print e
        print "Imported %s statuses and %s users" % (imported_statuses, imported_users)
