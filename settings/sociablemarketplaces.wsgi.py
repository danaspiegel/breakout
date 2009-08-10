import os, sys
import django.core.handlers.wsgi

project = os.path.dirname(os.path.dirname(__file__))
sys.path.append(project)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.sociablemarketplaces'

application = django.core.handlers.wsgi.WSGIHandler()
