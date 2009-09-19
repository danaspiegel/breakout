from models import *

class BreakoutMiddleware:
    def process_view(self, request, view_func, view_args, view_kwargs):
        """ 
        If the view uses a venue_slug, this adds the venue to the HttpRequest object
        If the view uses a session_format_slug, this adds the session_format to the HttpRequest object
        """
        venue_slug = view_kwargs.get('venue_slug')
        if venue_slug:
            request.venue = Venue.objects.get(slug=venue_slug)
        session_format_slug = view_kwargs.get('session_format_slug')
        if session_format_slug:
            request.session_format = BreakoutSessionFormat.objects.get(slug=session_format_slug)
