import datetime
import vobject

from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.encoding import smart_unicode, force_unicode
from django.views.decorators.cache import never_cache
from django.contrib.sites.models import Site

from ..models import Venue, BreakoutSession, BreakoutSessionFormat, SessionAttendance
from ..forms import BreakoutSessionForm

def index(request):
    today = datetime.datetime.utcnow()
    breakout_sessions = BreakoutSession.objects.filter(start_date__gte=datetime.datetime(today.year, today.month, today.day, 0, 0, 0)).order_by('start_date')
    return render_to_response('breakout_session/index.html', { 'breakout_sessions': breakout_sessions, }, context_instance=RequestContext(request))    

def list(request, session_format_slug=None, venue_slug=None, include_future=True, include_past=True):
    today = datetime.datetime.utcnow()
    past_breakout_sessions = BreakoutSession.objects.filter(start_date__lt=datetime.datetime(today.year, today.month, today.day, 0, 0, 0)).order_by('-start_date')[0:5]
    session_formats = BreakoutSessionFormat.objects.all().order_by('name')
    breakout_sessions = BreakoutSession.objects.all().order_by('end_date')
    if hasattr(request, 'session_format'):
        breakout_sessions = breakout_sessions.filter(session_format=request.session_format)
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

@never_cache
@login_required
def create(request):
    breakout_session = BreakoutSession(moderator=request.user)
    
    if request.method == 'POST':
        form = BreakoutSessionForm(request.POST, instance=breakout_session)
        if form.is_valid():
            breakout_session = form.save()            
            request.user.message_set.create(message="Session <strong>%s</strong> created" % breakout_session.name)
            if breakout_session.register(request.user):
                request.user.message_set.create(message="You have been registered for this Breakout Session")
            return HttpResponseRedirect(reverse('breakout_session_view', kwargs={ "breakout_session_id": breakout_session.id, "venue_slug": breakout_session.venue.slug }))
    else:
        form = BreakoutSessionForm(instance=breakout_session)
    return render_to_response('breakout_session/create.html', { 'form': form, }, context_instance=RequestContext(request))

@never_cache
@login_required
def register(request, venue_slug, breakout_session_id):
    """
    Registers a user for a session
    
    Session must be taking place, or scheduled for the future
    """
    try:
        breakout_session = BreakoutSession.objects.filter(venue=request.venue).get(pk=breakout_session_id)
        if breakout_session.register(request.user):
            request.user.message_set.create(message="You have been registered for this Breakout Session")
        return HttpResponseRedirect(reverse('breakout_session_view', kwargs={ "breakout_session_id": breakout_session.id, "venue_slug": breakout_session.venue.slug }))
    except BreakoutSession.DoesNotExist:
        request.user.message_set.create(message="Breakout Session does not exist")
        return HttpResponseRedirect(reverse('index'))

@never_cache
@login_required
def unregister(request, venue_slug, breakout_session_id):
    """
    Registers a user for a session
    """
    try:
        breakout_session = BreakoutSession.objects.filter(venue=request.venue).get(pk=breakout_session_id)
        if breakout_session.unregister(request.user):
            request.user.message_set.create(message="You have been un-registered for this Breakout Session")
        return HttpResponseRedirect(reverse('breakout_session_view', kwargs={ "breakout_session_id": breakout_session.id, "venue_slug": breakout_session.venue.slug }))
    except BreakoutSession.DoesNotExist:
        request.user.message_set.create(message="Breakout Session does not exist")
        return HttpResponseRedirect(reverse('index'))
    except SessionAttendance.DoesNotExist:
        request.user.message_set.create(message="You aren't registered for this Breakout Session")
        return HttpResponseRedirect(reverse('breakout_session_view', kwargs={ "breakout_session_id": breakout_session.id, "venue_slug": breakout_session.venue.slug }))

@never_cache
@login_required
def checkin(request, venue_slug, breakout_session_id):
    """
    Checks a user into a session
    """
    try:
        breakout_session = BreakoutSession.objects.filter(venue=request.venue).get(pk=breakout_session_id)
        if breakout_session.checkin(request.user):
            request.user.message_set.create(message="You have been checked into this Breakout Session")
        return HttpResponseRedirect(reverse('breakout_session_view', kwargs={ "breakout_session_id": breakout_session.id, "venue_slug": breakout_session.venue.slug }))
    except BreakoutSession.DoesNotExist:
        request.user.message_set.create(message="Breakout Session does not exist")
        return HttpResponseRedirect(reverse('index'))        

@never_cache
@login_required
def checkout(request, venue_slug, breakout_session_id):
    """
    Checks a user out of a session
    """
    try:
        breakout_session = BreakoutSession.objects.filter(venue=request.venue).get(pk=breakout_session_id)
        if breakout_session.checkout(request.user):
            request.user.message_set.create(message="You have been checked out of this Breakout Session")
        return HttpResponseRedirect(reverse('breakout_session_view', kwargs={ "breakout_session_id": breakout_session.id, "venue_slug": breakout_session.venue.slug }))
    except BreakoutSession.DoesNotExist:
        request.user.message_set.create(message="Breakout Session does not exist")
        return HttpResponseRedirect(reverse('index'))        

def ical(request):
    """
    Outputs an iCalendar response with all of the upcoming BreakoutSessions
    
    see http://blog.thescoop.org/archives/2007/07/31/django-ical-and-vobject/
    """
    calendar = vobject.iCalendar()
    calendar.add('method').value = 'PUBLISH'  # IE/Outlook needs this
    breakout_sessions = BreakoutSession.objects.all()
    for breakout_session in breakout_sessions:
        vevent = calendar.add('vevent')
        vevent.add('summary').value = breakout_session.name
        vevent.add('description').value = "%s\n\nSession Format: %s\nHosted By: %s" % (breakout_session.description, breakout_session.session_format.name, breakout_session.moderator.short_name, )
        vevent.add('url').value = "http://%s%s" % (Site.objects.get_current().domain, breakout_session.get_absolute_url(), )
        vevent.add('location').value = "%s - %s, %s, %s %s" % (breakout_session.venue.name, breakout_session.venue.street_address_1, breakout_session.venue.city, breakout_session.venue.state, breakout_session.venue.zip_code, )
        vevent.add('dtstart').value = breakout_session.start_date_localized
        vevent.add('dtend').value = breakout_session.end_date_localized
    icalendar_stream = calendar.serialize()
    response = HttpResponse(icalendar_stream, mimetype='text/calendar')
    response['Filename'] = 'breakout_sessions.ics'  # IE needs this
    response['Content-Disposition'] = 'attachment; filename=breakout_sessions.ics'
    return response
