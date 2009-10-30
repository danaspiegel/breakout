import datetime
import pytz

from django.conf import settings
from django import forms
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

class BreakoutSessionForm(forms.ModelForm):    
    start_date = forms.DateTimeField(label='Starting Date and Time', input_formats=('%m/%d/%Y %I:%M %p', ))
    end_date = forms.DateTimeField(label='Ending Date and Time', input_formats=('%m/%d/%Y %I:%M %p', ))
    session_format = forms.ModelChoiceField(queryset=BreakoutSessionFormat.objects.all().order_by('name'))
    
    def clean(self):
        super(BreakoutSessionForm, self).clean()
        cleaned_data = self.cleaned_data
        if not ('start_date' in cleaned_data) or not ('end_date' in cleaned_data) or not ('timezone' in cleaned_data):
            # there are missing fields, so just return since the required fields already have errors
            return self.cleaned_data
        
        # get the declared timezone
        timezone = pytz.timezone(cleaned_data['timezone'])
        
        # make sure that the start_date is before the end_date
        
        # localize the start_date using the timezone
        localized_start_date = timezone.localize(cleaned_data['start_date'])
        # convert the start_date to UTC
        utc_start_date = localized_start_date.astimezone(pytz.utc)
        # recreate the start_date stripping the timezone (since we can't have a timezone)
        cleaned_utc_start_date = datetime.datetime(utc_start_date.year, utc_start_date.month, utc_start_date.day, utc_start_date.hour, utc_start_date.minute)
        cleaned_data['start_date'] = cleaned_utc_start_date
        print cleaned_utc_start_date
        # localize the end_date using the timezone
        localized_end_date = timezone.localize(cleaned_data['end_date'])
        # convert the end_date to UTC
        utc_end_date = localized_end_date.astimezone(pytz.utc)
        # recreate the end_date stripping the timezone (since we can't have a timezone)
        cleaned_utc_end_date = datetime.datetime(utc_end_date.year, utc_end_date.month, utc_end_date.day, utc_end_date.hour, utc_end_date.minute)
        cleaned_data['end_date'] = cleaned_utc_end_date
        
        return cleaned_data
    
    class Meta:
        model = BreakoutSession
        exclude = ('moderator', 'registered_users', )
        # fields = ('name', 'description', 'start_date', 'end_date', 'venue', 'session_format', 'available_spots', )
