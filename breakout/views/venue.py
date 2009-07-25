from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.encoding import smart_unicode, force_unicode

from ..models import Venue

def list(request):
    venues = Venue.objects.all().order_by('-created_on')
    return render_to_response('venue/list.html', { 'venues': venues }, context_instance=RequestContext(request))

def view(request, venue_slug):
    try:
        venue = Venue.objects.get(slug=venue_slug)
        return render_to_response('venue/view.html', { 'venue': venue }, context_instance=RequestContext(request))
    except Venue.DoesNotExist:
        return HttpResponseRedirect(reverse('index'))        
