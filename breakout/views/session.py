import datetime

from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.encoding import smart_unicode, force_unicode

from ..models import Venue, BreakoutSession, BreakoutCategory

def index(request):
    today = datetime.datetime.today()
    breakout_sessions = BreakoutSession.objects.filter(start_date__gte=datetime.datetime(today.year, today.month, today.day, 0, 0, 0)).order_by('start_date')
    past_breakout_sessions = BreakoutSession.objects.filter(start_date__lt=datetime.datetime(today.year, today.month, today.day, 0, 0, 0)).order_by('-start_date')[0:5]
    categories = BreakoutCategory.objects.all().order_by('name')
    return render_to_response('breakout_session/index.html', { 'breakout_sessions': breakout_sessions, 'past_breakout_sessions': past_breakout_sessions, 'categories': categories, }, context_instance=RequestContext(request))    

def list(request, category_slug=None, venue_slug=None, include_future=True, include_past=True):
    breakout_sessions = BreakoutSession.objects.all().order_by('-created_on')
    if category_slug:
        category = BreakoutCategory.objects.get(slug=category_slug)
        breakout_sessions = breakout_sessions.filter(category=category)
    else:
        category = None
    if venue_slug:
        venue = Venue.objects.get(slug=venue_slug)
        breakout_sessions = breakout_sessions.filter(venue=venue)
    else:
        venue = None
    if not include_past:
        today = datetime.datetime.today()
        breakout_sessions = breakout_sessions.filter(start_date__gte=datetime.datetime(today.year, today.month, today.day, 0, 0, 0))
    elif not include_future:
        today = datetime.datetime.today()
        breakout_sessions = breakout_sessions.filter(start_date__lt=datetime.datetime(today.year, today.month, today.day, 0, 0, 0))
    return render_to_response('breakout_session/list.html', 
                                { 'breakout_sessions': breakout_sessions, 
                                  'category': category, 
                                  'venue': venue, 
                                  'include_future': include_future,
                                  'include_past': include_past, }, 
                                context_instance=RequestContext(request))    

def view(request, venue_slug, session_id):
    try:
        venue = Venue.objects.get(slug=venue_slug)
        breakout_session = BreakoutSession.objects.filter(venue=venue).get(pk=session_id)
        return render_to_response('breakout_session/view.html', { 'breakout_session': breakout_session, 'venue': venue }, context_instance=RequestContext(request))
    except BreakoutSession.DoesNotExist:
        return HttpResponseRedirect(reverse('index'))        
    except Venue.DoesNotExist:
        return HttpResponseRedirect(reverse('index'))
