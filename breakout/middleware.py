from models import *

class BreakoutMiddleware:
    def process_view(self, request, view_func, view_args, view_kwargs):
        """ 
        If the view uses a venue_slug, this adds the venue to the HttpRequest object
        If the view uses a category_slug, this adds the category to the HttpRequest object
        """
        venue_slug = view_kwargs.get('venue_slug')
        if venue_slug:
            request.venue = Venue.objects.get(slug=venue_slug)
        category_slug = view_kwargs.get('category_slug')
        if category_slug:
            request.category = BreakoutSessionFormat.objects.get(slug=category_slug)
