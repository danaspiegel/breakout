import datetime

from models import *

def sidebar(request):
    """ adds past_breakout_sessions and session_formats to the RequestContext for use in template rendering """
    breakout_dictionary = {}
    today = datetime.datetime.utcnow()
    past_breakout_sessions = BreakoutSession.objects.filter(start_date__lt=datetime.datetime(today.year, today.month, today.day, 0, 0, 0))
    if hasattr(request, "venue"):
        past_breakout_sessions = past_breakout_sessions.filter(venue=request.venue)
    breakout_dictionary['past_breakout_sessions'] = past_breakout_sessions.order_by('-start_date')[0:5]
    breakout_dictionary['session_formats'] = BreakoutSessionFormat.objects.all().order_by('name')
    if hasattr(request, 'venue'):
        breakout_dictionary['venue'] = request.venue
    if hasattr(request, 'session_format'):
        breakout_dictionary['session_format'] = request.session_format
    return breakout_dictionary
