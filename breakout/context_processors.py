import datetime

from models import *

def sidebar(request):
    """ adds past_breakout_sessions and categories to the RequestContext for use in template rendering """
    breakout_dictionary = {}
    today = datetime.datetime.today()
    past_breakout_sessions = BreakoutSession.objects.filter(start_date__lt=datetime.datetime(today.year, today.month, today.day, 0, 0, 0))
    if hasattr(request, "venue"):
        past_breakout_sessions = past_breakout_sessions.filter(venue=request.venue)
    breakout_dictionary['past_breakout_sessions'] = past_breakout_sessions.order_by('-start_date')[0:5]
    breakout_dictionary['categories'] = BreakoutCategory.objects.all().order_by('name')
    if hasattr(request, 'venue'):
        breakout_dictionary['venue'] = request.venue
    if hasattr(request, 'category'):
        breakout_dictionary['category'] = request.category
    return breakout_dictionary
