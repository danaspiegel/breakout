
from south.db import db
from django.db import models
from breakout.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'Venue.latitude'
        db.add_column('breakout_venue', 'latitude', orm['breakout.Venue:latitude'])
        
        # Adding field 'Venue.longitude'
        db.add_column('breakout_venue', 'longitude', orm['breakout.Venue:longitude'])
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'Venue.latitude'
        db.delete_column('breakout_venue', 'latitude')
        
        # Deleting field 'Venue.longitude'
        db.delete_column('breakout_venue', 'longitude')
        
    
    
    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'breakout.breakoutsessionformat': {
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '20'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True', 'db_index': 'True'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'breakout.breakoutsession': {
            'available_spots': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'session_format': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'breakout_sessions'", 'to': "orm['breakout.BreakoutSessionFormat']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moderator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'moderating_sessions'", 'to': "orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'registered_users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']"}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'breakout_sessions'", 'to': "orm['breakout.Venue']"})
        },
        'breakout.sessionattendance': {
            'arrival_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'departure_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'registrant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'session_attendance'", 'to': "orm['auth.User']"}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'session_attendance'", 'to': "orm['breakout.BreakoutSession']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'R'", 'max_length': '1'})
        },
        'breakout.venue': {
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone_number': ('django.contrib.localflavor.us.models.PhoneNumberField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True', 'db_index': 'True'}),
            'state': ('django.contrib.localflavor.us.models.USStateField', [], {}),
            'street_address_1': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'street_address_2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }
    
    complete_apps = ['breakout']
