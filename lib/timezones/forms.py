"""Custom form for a time zone-aware model field.

Contains portions from Django's django.forms.fields module.
"""
from datetime import date, datetime, timedelta, tzinfo
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.forms.fields import EMPTY_VALUES, DEFAULT_DATETIME_INPUT_FORMATS
from django.utils.translation import ugettext_lazy as _
import pytz
import re
import time


# 2009-06-04 12:00:00+01:00 or 2009-06-04 12:00:00 +0100
TZ_INFO = re.compile(r'^(.*?)(?:\s?([-\+])(\d\d):?(\d\d))?$')


class TZDateTimeField(forms.DateTimeField):
    def clean(self, value):
        """Cleans a datetime value.
        
        The datetime instance will be in UTC if there is time zone information.

        >>> field = TZDateTimeField()
        >>> field.clean('')     #doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
          ...
        ValidationError: <django.utils.functional.__proxy__ object at 0x10be4f0>
        >>> field.clean('2009-07-02')
        datetime.datetime(2009, 7, 2, 0, 0)
        >>> field.clean('2009-07-02 12:00')
        datetime.datetime(2009, 7, 2, 12, 0)
        >>> field.clean('2009-07-02 15:00:30+0300')
        datetime.datetime(2009, 7, 2, 12, 0, 30, tzinfo=<UTC>)
        >>> field.clean('2009-07-02 09:00:30-0300')
        datetime.datetime(2009, 7, 2, 12, 0, 30, tzinfo=<UTC>)
        >>> field.clean('07/02/2009')
        datetime.datetime(2009, 7, 2, 0, 0)
        >>> field.clean('7/2/09')
        datetime.datetime(2009, 7, 2, 0, 0)
        >>> field.clean('2.7.2009')
        Traceback (most recent call last):
          ...
        ValidationError: Not a valid datetime string
        >>> field = TZDateTimeField(required=False)
        >>> field.clean('')
        >>> field = TZDateTimeField(required=False, input_formats=['%d/%m/%y'])
        >>> field.clean('2/7/09')
        datetime.datetime(2009, 7, 2, 0, 0)
        """
        if self.required and value in EMPTY_VALUES:
            raise ValidationError(self.error_messages['required'])
            
        if isinstance(value, list):
            # Input comes from a SplitDateTimeWidget, for example. So, it's two
            # components: date and time.
            if len(value) != 2:
                raise ValidationError(self.error_messages['invalid'])
            value = '%s %s' % tuple(value)
        try:
            return parse_dt(value, formats=self.input_formats)
        except ValueError:
            raise ValidationError, "Please enter using valid date time format"
        

def parse_tzdt(value, formats=None):
    """Returns a time zone-aware datetime or None."""
    value = parse_dt(value, formats)
    if value is None:
        return value
    if (value.tzinfo is None) or (value.tzinfo.utcoffset(value) is None):
        value = force_tz(value, settings.TIME_ZONE)
    return value
    
    
def split_tz_info(value):
    """Returns a tuple of strings (datestring, tzoperator, tzhours, tzmins) for
    a datetime string. Raises ValueError if the string does not match.
    
    tzoperator, tzhours and tzmins will be None if there was no timezone info.

    >>> split_tz_info('2009-07-01 12:00 +00:00')
    ('2009-07-01 12:00', '+', '00', '00')
    >>> split_tz_info('2009-07-01 12:00 -00:00')
    ('2009-07-01 12:00', '-', '00', '00')
    >>> split_tz_info('2009-07-01 12:00 -0000')
    ('2009-07-01 12:00', '-', '00', '00')
    >>> split_tz_info('2009-07-01 12:00-0000')
    ('2009-07-01 12:00', '-', '00', '00')
    >>> split_tz_info('2009-07-01 12:00:30 -0000')
    ('2009-07-01 12:00:30', '-', '00', '00')
    >>> split_tz_info('2009-07-01')
    ('2009-07-01', None, None, None)
    >>> split_tz_info('')
    ('', None, None, None)
    """
    match = TZ_INFO.search(value)
    if match:
        value, tzop, tzhours, tzmins = match.groups()
        return value, tzop, tzhours, tzmins
    else:
        raise ValueError, "Not a valid datetime string"
    
    
def parse_dt(value, formats=None):
    """Returns a datetime for a string, possibly time zone-aware.
    
    Raises ValidationError if the value is not a valid date time. If the string
    ends with '[-+]hh:mm' then it is converted to UTC. formats is a sequence
    of datetime formats suitable for use with time.strptime(<date>, <format>),
    it defaults to Django's built-in format list.
   
    >>> parse_dt('2009-07-01')
    datetime.datetime(2009, 7, 1, 0, 0)
    >>> parse_dt('2009-07-01 12:00')
    datetime.datetime(2009, 7, 1, 12, 0)
    >>> parse_dt('2009-07-01 12:00:45')
    datetime.datetime(2009, 7, 1, 12, 0, 45)
    >>> parse_dt('2009-07-01 12:00:45 +0100')
    datetime.datetime(2009, 7, 1, 11, 0, 45, tzinfo=<UTC>)
    >>> parse_dt('2009-07-01 12:00:45 -0100')
    datetime.datetime(2009, 7, 1, 13, 0, 45, tzinfo=<UTC>)
    >>> parse_dt('2009-07-01 12:00-01:00')
    datetime.datetime(2009, 7, 1, 13, 0, tzinfo=<UTC>)
    >>> parse_dt('5/12/2009 12:00-01:00')
    datetime.datetime(2009, 5, 12, 13, 0, tzinfo=<UTC>)
    """
    if value in EMPTY_VALUES:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, date):
        return datetime(value.year, value.month, value.day)
        
    value, tzop, tzhours, tzmins = split_tz_info(value)
    # At this point value should be just the date portion
    # split usecs, because they are not recognized by strptime.
    if '.' in value:
        try:
            value, usecs = value.split('.')
            usecs = int(usecs)
        except ValueError:
            raise ValidationError, "Not a valid datetime string"
    else:
        usecs = 0
    kwargs = {'microsecond': usecs}
    formats = formats or DEFAULT_DATETIME_INPUT_FORMATS
    for fmt in formats:
        try:
            value = datetime(*time.strptime(value, fmt)[:6], **kwargs)
            break
        except ValueError:
            pass
    else:
        raise ValidationError, "Not a valid datetime string"

    # value matched one of the datetime formats, now convert tz information
    if tzop:
        value = value - timedelta(hours=int(tzop + tzhours), minutes=int(tzop + tzmins))
        value = value.replace(tzinfo=pytz.utc)

    return value


# Cache return values when looking up pytz.timezone(<tzname>)
_TZ_CACHE = {}

def force_tz(obj, tz):
    """Converts a datetime to the given timezone.
    
    The tz argument can be an instance of tzinfo or a string such as
    'Europe/London' that will be passed to pytz.timezone. Naive datetimes are
    forced to the timezone. Wise datetimes are converted.
    """
    global _TZ_CACHE
    if not isinstance(tz, tzinfo):
        if tz not in _TZ_CACHE:
            _TZ_CACHE[tz] = pytz.timezone(tz)
        tz = _TZ_CACHE[tz]

    if (obj.tzinfo is None) or (obj.tzinfo.utcoffset(obj) is None):
        return tz.localize(obj)
    else:
        return obj.astimezone(tz)
