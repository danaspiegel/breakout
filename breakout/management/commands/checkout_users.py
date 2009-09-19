"""
checkout_users.py

Marks users as checked out of a BreakoutSession when a Session is over

"""

import datetime
from dateutil.relativedelta import *
from django.core.management.base import CommandError, NoArgsCommand
from django.conf import settings

from ...models import BreakoutSession, SessionAttendance

class Command(NoArgsCommand):    
    def handle_noargs(self, **options):
        # for all breakout sessions that finished in the last day
        now = datetime.datetime.utcnow()
        yesterday = now - relativedelta(days=1)
        breakout_sessions = BreakoutSession.objects.filter(end_date__gt=yesterday, end_date__lt=now)
        for breakout_session in breakout_sessions:
            print "Cleaning up recently ended Breakout Session: %s (%s)" % (breakout_session.name, breakout_session.id, )
            # We use current_participants because it is defined as people who have no checkout date
            for user in breakout_session.current_participants:
                print "  Checking out user: %s" % user
                session_attendance = user.session_attendance.get(session=breakout_session)
                session_attendance.departure_time = breakout_session.end_date
                session_attendance.save()
