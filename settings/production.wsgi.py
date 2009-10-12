import os, sys
import django.core.handlers.wsgi

project = os.path.dirname(os.path.dirname(__file__))
sys.path.append(project)
sys.stdout = sys.stderr

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'

application = django.core.handlers.wsgi.WSGIHandler()
