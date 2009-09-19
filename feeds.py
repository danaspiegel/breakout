import datetime

from django.contrib.syndication.feeds import Feed

import breakout.models

class BreakoutSessionsFeed(Feed):
    title = "Breakout! Festival Session Feed"
    link = "/sessions/"
    description = "Breakout! Festival's sessions"

    def items(self):
        now = datetime.datetime.utcnow()
        return breakout.models.BreakoutSession.objects.filter(start_date__gte=now).order_by('start_date')[:20]

feeds = {
    'sessions': BreakoutSessionsFeed,
}

