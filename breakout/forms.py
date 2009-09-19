import datetime, random, re, calendar

from django.conf import settings
from django.forms import *
from django.forms.formsets import *
from django.forms.util import ErrorList
from django.utils.translation import ugettext as _
from django.utils.html import escape, conditional_escape
from django.utils.safestring import mark_safe
from django.utils.encoding import StrAndUnicode, force_unicode
from django.contrib.sites.models import Site
from django.contrib.auth.models import *
from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string
from django.db.models import Q

from models import *

class BreakoutSessionForm(ModelForm):    
    class Meta:
        model = BreakoutSession
        fields = ('name', 'description', 'session_format', 'start_date', 'end_date', 'venue', 'available_spots', )
