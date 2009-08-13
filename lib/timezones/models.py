from datetime import datetime
from django.db import models
from timezones.fields import TZDateTimeField


class Article(models.Model):
    pub_date = TZDateTimeField(default=datetime.now)
    
    class Meta:
        db_table = 'timezones_articletest'
        