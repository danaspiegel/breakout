import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.encoding import smart_unicode, force_unicode

from ..models import Venue, BreakoutSession, BreakoutCategory, SessionAttendance
from ..forms import BreakoutSessionForm

def index(request):
    today = datetime.datetime.today()
    breakout_sessions = BreakoutSession.objects.filter(start_date__gte=datetime.datetime(today.year, today.month, today.day, 0, 0, 0)).order_by('start_date')
    return render_to_response('breakout_session/index.html', { 'breakout_sessions': breakout_sessions, }, context_instance=RequestContext(request))    

def list(request, category_slug=None, venue_slug=None, include_future=True, include_past=True):
    today = datetime.datetime.today()
    past_breakout_sessions = BreakoutSession.objects.filter(start_date__lt=datetime.datetime(today.year, today.month, today.day, 0, 0, 0)).order_by('-start_date')[0:5]
    categories = BreakoutCategory.objects.all().order_by('name')
    breakout_sessions = BreakoutSession.objects.all().order_by('-end_date')
    if hasattr(request, 'category'):
        breakout_sessions = breakout_sessions.filter(category=request.category)
    if hasattr(request, 'venue'):
        breakout_sessions = breakout_sessions.filter(venue=request.venue)
    if not include_past:
        breakout_sessions = breakout_sessions.filter(start_date__gte=datetime.datetime(today.year, today.month, today.day, 0, 0, 0))
    elif not include_future:
        breakout_sessions = breakout_sessions.filter(end_date__lt=datetime.datetime(today.year, today.month, today.day, 0, 0, 0))
    return render_to_response('breakout_session/list.html', 
                                { 'breakout_sessions': breakout_sessions, 
                                  'include_future': include_future,
                                  'include_past': include_past, }, 
                                context_instance=RequestContext(request))    

def view(request, venue_slug, breakout_session_id):
    try:
        breakout_session = BreakoutSession.objects.filter(venue=request.venue).get(pk=breakout_session_id)
        return render_to_response('breakout_session/view.html', { 'breakout_session': breakout_session }, context_instance=RequestContext(request))
    except BreakoutSession.DoesNotExist:
        return HttpResponseRedirect(reverse('index'))        
    except Venue.DoesNotExist:
        return HttpResponseRedirect(reverse('index'))

@login_required
def create(request):
    breakout_session = BreakoutSession(moderator=request.user)
    
    if request.method == 'POST':
        form = BreakoutSessionForm(request.POST, instance=breakout_session)
        if form.is_valid():            
            breakout_session = form.save()            
            request.user.message_set.create(message="Session <strong>%s</strong> created" % breakout_session.name)
            return HttpResponseRedirect(reverse('breakout_session_view', kwargs={ "breakout_session_id": breakout_session.id, "venue_slug": breakout_session.venue.slug }))
    else:
        form = BreakoutSessionForm(instance=breakout_session)
    return render_to_response('breakout_session/create.html', { 'form': form, }, context_instance=RequestContext(request))

@login_required
def checkin(request, venue_slug, breakout_session_id):
    """
    Checks a user into a session
    """
    try:
        breakout_session = BreakoutSession.objects.get(pk=breakout_session_id)
        session_attendance, created = SessionAttendance.objects.get_or_create(registrant=request.user, session=breakout_session)
        session_attendance.status = 'P'
        session_attendance.arrival_time = datetime.datetime.now()
        session_attendance.save()
        return HttpResponseRedirect(reverse('breakout_session_view', kwargs={ "breakout_session_id": breakout_session.id, "venue_slug": breakout_session.venue.slug }))
    except BreakoutSession.DoesNotExist:
        request.user.message_set.create(message="Breakout Session does not exist")
        return HttpResponseRedirect(reverse('index'))        
    