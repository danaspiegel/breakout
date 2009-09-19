import datetime

from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.encoding import smart_unicode, force_unicode

from ..models import Venue, BreakoutSession

def list(request):
    venues = Venue.objects.all().order_by('-created_on')
    return render_to_response('venue/list.html', { 'venues': venues }, context_instance=RequestContext(request))

def view(request, venue_slug):
    return render_to_response('venue/view.html', context_instance=RequestContext(request))

def archive(request, session_format_slug=None, venue_slug=None):
    today = datetime.datetime.today()
    breakout_sessions = BreakoutSession.objects.filter(end_date__lt=datetime.datetime(today.year, today.month, today.day, 0, 0, 0)).order_by('-end_date')
    if hasattr(request, 'session_format'):
        breakout_sessions = breakout_sessions.filter(session_format=request.session_format)
    if hasattr(request, 'venue'):
        breakout_sessions = breakout_sessions.filter(venue=request.venue)
    return render_to_response('venue/archive.html', { 'breakout_sessions': breakout_sessions, }, context_instance=RequestContext(request))    
