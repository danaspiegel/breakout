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
    try:
        venue = Venue.objects.get(slug=venue_slug)
        return render_to_response('venue/view.html', { 'venue': venue }, context_instance=RequestContext(request))
    except Venue.DoesNotExist:
        return HttpResponseRedirect(reverse('index'))        

def archive(request, category_slug=None, venue_slug=None):
    today = datetime.datetime.today()
    breakout_sessions = BreakoutSession.objects.filter(end_date__lt=datetime.datetime(today.year, today.month, today.day, 0, 0, 0)).order_by('-end_date')
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
    return render_to_response('venue/archive.html', 
                                { 'breakout_sessions': breakout_sessions, 
                                  'category': category, 
                                  'venue': venue, }, 
                                context_instance=RequestContext(request))    
