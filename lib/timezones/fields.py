"""A time zone-aware DateTime field.

When saving, naive datetime objects are assumed to belong to the local time
zone and are converted to UTC. When loading from the database the naive datetime
objects are converted to UTC.

These field types require database support. MySQL 5 will not work.
"""
from datetime import datetime
from django.conf import settings
from django.db import models
from timezones.forms import TZDateTimeField as TZFormField, parse_tzdt
import pytz


class TZDatetime(datetime):
    def aslocaltimezone(self):
        """Returns the datetime in the local time zone."""
        tz = pytz.timezone(settings.TIME_ZONE)
        return self.astimezone(tz)


class TZDateTimeField(models.DateTimeField):
    """A DateTimeField that treats naive datetimes as local time zone."""
    __metaclass__ = models.SubfieldBase
    
    def to_python(self, value):
        """Returns a time zone-aware datetime object.
        
        This ignores Django's parsing since we need to re-implement most of it
        for validating form fields anyway.
        """
        value = parse_tzdt(value)        
        if value is None:
            return value
            
        return TZDatetime(value.year, value.month, value.day, value.hour,
            value.minute, value.second, value.microsecond, tzinfo=value.tzinfo)
     
    def formfield(self, **kwargs):
        defaults = {'form_class': TZFormField}
        defaults.update(kwargs)
        return super(TZDateTimeField, self).formfield(**defaults)
        
        
    
    
        