"""
>>> import pytz
>>> from datetime import datetime
>>> from django.conf import settings
>>> from django.db import close_connection
>>> from timezones.models import Article

# Save the time zone. This test mostly assumes Europe/London
>>> original_zone = settings.TIME_ZONE
>>> settings.TIME_ZONE = 'Europe/London'
>>> close_connection()

>>> london = pytz.timezone('Europe/London')
>>> mauritius = pytz.timezone('Indian/Mauritius')
>>> dt1 = london.localize(datetime(2009, 6, 4, 12, 0, 0))
>>> dt1
datetime.datetime(2009, 6, 4, 12, 0, tzinfo=<DstTzInfo 'Europe/London' BST+1:00:00 DST>)

# Wise datetimes are converted to UTC
>>> article = Article(pub_date=dt1)
>>> article.pub_date
TZDatetime(2009, 6, 4, 12, 0, tzinfo=<DstTzInfo 'Europe/London' BST+1:00:00 DST>)
>>> dt2 = dt1.astimezone(mauritius)
>>> dt2
datetime.datetime(2009, 6, 4, 15, 0, tzinfo=<DstTzInfo 'Indian/Mauritius' MUT+4:00:00 STD>)

# Mauritius is 4 hours ahead of UTC
>>> article = Article(pub_date=dt2)
>>> article.pub_date
TZDatetime(2009, 6, 4, 15, 0, tzinfo=<DstTzInfo 'Indian/Mauritius' MUT+4:00:00 STD>)

# Same time in different zones compare equal
>>> article.pub_date
TZDatetime(2009, 6, 4, 15, 0, tzinfo=<DstTzInfo 'Indian/Mauritius' MUT+4:00:00 STD>)
>>> dt1
datetime.datetime(2009, 6, 4, 12, 0, tzinfo=<DstTzInfo 'Europe/London' BST+1:00:00 DST>)
>>> article.pub_date == dt1
True

# Naive datetimes are converted in the default time zone
>>> settings.TIME_ZONE = 'Indian/Mauritius'
>>> article = Article(pub_date=datetime(2009, 6, 4, 15, 0))
>>> article.pub_date
TZDatetime(2009, 6, 4, 15, 0, tzinfo=<DstTzInfo 'Indian/Mauritius' MUT+4:00:00 STD>)

# UTCDateTimeField parses text as dates
>>> Article(pub_date='2009-06-04 15:00:00').pub_date
TZDatetime(2009, 6, 4, 15, 0, tzinfo=<DstTzInfo 'Indian/Mauritius' MUT+4:00:00 STD>)

# Time zone in the string can be '+HHMM' for east of UTC
>>> Article(pub_date='2009-06-04 12:00:00 +0100').pub_date
TZDatetime(2009, 6, 4, 11, 0, tzinfo=<UTC>)
>>> Article(pub_date='2009-06-04 15:00:00 +0400').pub_date
TZDatetime(2009, 6, 4, 11, 0, tzinfo=<UTC>)

# The space before the offset is optional
>>> Article(pub_date='2009-06-04 12:00:00+0100').pub_date
TZDatetime(2009, 6, 4, 11, 0, tzinfo=<UTC>)

# The offset HH and MM can be separated by a colon
>>> Article(pub_date='2009-06-04 12:00:00+01:00').pub_date
TZDatetime(2009, 6, 4, 11, 0, tzinfo=<UTC>)

# Works for times west of UTC as well
>>> Article(pub_date='2009-06-04 06:00:00-05:00').pub_date
TZDatetime(2009, 6, 4, 11, 0, tzinfo=<UTC>)

# But cannot handle timezone codes like CET and BST
>>> Article(pub_date='2009-06-04 12:00:00 BST+0100').pub_date
Traceback (most recent call last):
    ...
ValidationError: Not a valid datetime string

# date field survives being saved to the database
>>> settings.TIME_ZONE = 'Europe/London'
>>> close_connection()
>>> article = Article(pub_date='2009-06-04 12:00:00+0100')
>>> article.pub_date
TZDatetime(2009, 6, 4, 11, 0, tzinfo=<UTC>)
>>> article.save()
>>> pk = article.pk
>>> assert pk
>>> article2 = Article.objects.get(pk=pk)
>>> article2.pub_date
TZDatetime(2009, 6, 4, 12, 0, tzinfo=<DstTzInfo 'Europe/London' BST+1:00:00 DST>)

# TZDatetime instances provide aslocaltimezone to convert to local time zone
>>> article2.pub_date
TZDatetime(2009, 6, 4, 12, 0, tzinfo=<DstTzInfo 'Europe/London' BST+1:00:00 DST>)
>>> article2.pub_date.aslocaltimezone()
datetime.datetime(2009, 6, 4, 12, 0, tzinfo=<DstTzInfo 'Europe/London' BST+1:00:00 DST>)

>>> settings.TIME_ZONE = original_zone

# You can change the time zone if you close the database connection first
>>> settings.TIME_ZONE
'Europe/London'
>>> before = Article.objects.get(pk=pk)
>>> before.pub_date
TZDatetime(2009, 6, 4, 12, 0, tzinfo=<DstTzInfo 'Europe/London' BST+1:00:00 DST>)
>>> close_connection()
>>> settings.TIME_ZONE = 'Indian/Mauritius'
>>> after = Article.objects.get(pk=pk)
>>> after.pub_date
TZDatetime(2009, 6, 4, 15, 0, tzinfo=<DstTzInfo 'Indian/Mauritius' MUT+4:00:00 STD>)

# Setting TZDatetimeField to None is OK
>>> a = Article(pub_date=None)
>>> a.pub_date
>>> 

# Default arguments to Article.pub_date should use the project time zone
>>> a = Article()
>>> a.pub_date.tzinfo.zone
'Indian/Mauritius'
>>> a.pub_date.tzinfo.zone == settings.TIME_ZONE
True

>>> close_connection()
>>> settings.TIME_ZONE = original_zone

"""