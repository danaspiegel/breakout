import os.path
import re

from django.conf import settings

class iPhoneMiddleware(object):
    """
    If the Middleware detects an iPhone/iPod the template dir changes to the
    iPhone template folder.
    
    from http://bernde.wordpress.com/2008/11/14/detection-for-iphone-django/
    """
    
    def __init__(self):
        self.normal_templates = settings.TEMPLATE_DIRS
        self.iphone_templates = (os.path.join(settings.TEMPLATE_DIRS[0], 'iphone'), ) + settings.TEMPLATE_DIRS
    
    def process_request(self, request):
        p = re.compile('iPhone|iPod', re.IGNORECASE)
        if p.search(request.META['HTTP_USER_AGENT']):
            # user agent looks like iPhone or iPod
            settings.TEMPLATE_DIRS = self.iphone_templates
        else:
            # other user agents
            settings.TEMPLATE_DIRS = self.normal_templates
        return
