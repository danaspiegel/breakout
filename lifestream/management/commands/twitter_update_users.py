import datetime
import time
from dateutil.parser import parse
from django.core.management.base import CommandError, NoArgsCommand
from django.conf import settings

import pytwitter
import simplejson

from ...models import TwitterUser

class Command(NoArgsCommand):    
    def handle_noargs(self, **options):
        updated_users = 0
        api = pytwitter.pytwitter()
        
        twitter_users = TwitterUser.objects.all().order_by('updated_on')
        for twitter_user in twitter_users:
            print "Checking user: %s" % twitter_user.screen_name
            try:
                user_details_json = api.users_show(id=twitter_user.screen_name)
                twitter_user.update_from_twitter(simplejson.loads(user_details_json))
                # TODO: this should check to see if the user really needs to be saved again
                twitter_user.save()
                updated_users += 1
            except pytwitter.TwitterError, e:
                if e.code == 404:
                    pass
                    # FIXME!!
                    # GETTING EXCEPTION:
                    # AttributeError: 'TwitterUser' object has no attribute 'statuses'
                    # print "Deleting hidden user or suspended user (%s): %s" % (e.error, twitter_user.screen_name) 
                    # twitter_user.statuses.all().delete()
                    # twitter_user.delete()
                else:
                    print "Exception for %s: %s" % (twitter_user.screen_name, e)
        print "Updated %s users" % (updated_users)
