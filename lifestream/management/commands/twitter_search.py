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
import dateutil.parser
from django.core.management.base import CommandError, NoArgsCommand
from django.conf import settings

import pytwitter
import simplejson

from ...models import TwitterUser, TwitterStatus
import breakout.models

class Command(NoArgsCommand):    
    def handle_noargs(self, **options):
        imported_statuses = 0
        api = pytwitter.pytwitter()
        search_api = pytwitter.pytwitter(url='http://search.twitter.com')
        
        # Get a list of all active sessions
        now = datetime.datetime.now()
        breakout_sessions = breakout.models.BreakoutSession.objects.filter(start_date__lte=now, end_date__gte=now)
        
        # for each active breakout session, iterate through the attending_users
        for breakout_session in breakout_sessions:
            print 'Looking at BreakoutSession: %s (%s)' % (breakout_session.name, breakout_session.id, )
            # for all participants in a session
            for user in breakout_session.participants:
                # if the user has a TwitterUser that's not muted
                session_attendance = breakout.models.SessionAttendance.objects.get(registrant=user, session=breakout_session)
                twitter_user = user.get_profile().twitter_user
                if not twitter_user:
                    print '  User has no TwitterUser: %s' % (user.short_name, )
                    continue
                print '  Looking at User (screen_name): %s (%s) (muted: %s)' % (user.short_name, twitter_user.screen_name, twitter_user.is_muted)
                # make sure that the twitter_user isn't muted
                if not twitter_user.is_muted:
                    # get the paged twitter statuses
                    for page in xrange(1, 15):
                        try:
                            response_json = api.statuses_user_timeline(screen_name=twitter_user.screen_name, page=page, rpp=100, format='json')
                            response = simplejson.loads(response_json)
                            if len(response) == 0: break
                            print '    Parsing page %s' % page
                            for result in response:
                                # make sure we are only importing statuses that are created while the user is active
                                created_on = dateutil.parser.parse(result['created_at'], ignoretz=True)
                                if session_attendance.is_during(created_on):
                                    print '    Status is during breakout session: %s' % created_on
                                    twitter_status, created = TwitterStatus.objects.get_or_create(twitter_id=result['id'], twitter_user=twitter_user, user=user, breakout_session=breakout_session)
                                    if created:
                                        imported_statuses = imported_statuses + 1
                                        twitter_status.twitter_user = twitter_user
                                        twitter_status.text = result['text']
                                        twitter_status.created_on = created_on
                                        twitter_status.location = twitter_user.location
                                        twitter_status.save()
                        except Exception, e:
                            print e
        print "Imported %s statuses" % (imported_statuses, )
