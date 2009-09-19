
from south.db import db
from django.db import models
from breakout.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'BreakoutSession'
        db.create_table('breakout_breakoutsession', (
            ('id', orm['breakout.BreakoutSession:id']),
            ('created_on', orm['breakout.BreakoutSession:created_on']),
            ('updated_on', orm['breakout.BreakoutSession:updated_on']),
            ('name', orm['breakout.BreakoutSession:name']),
            ('description', orm['breakout.BreakoutSession:description']),
            ('session_format', orm['breakout.BreakoutSession:session_format']),
            ('start_date', orm['breakout.BreakoutSession:start_date']),
            ('end_date', orm['breakout.BreakoutSession:end_date']),
            ('moderator', orm['breakout.BreakoutSession:moderator']),
            ('venue', orm['breakout.BreakoutSession:venue']),
            ('available_spots', orm['breakout.BreakoutSession:available_spots']),
        ))
        db.send_create_signal('breakout', ['BreakoutSession'])
        
        # Adding model 'SessionAttendance'
        db.create_table('breakout_sessionattendance', (
            ('id', orm['breakout.SessionAttendance:id']),
            ('registrant', orm['breakout.SessionAttendance:registrant']),
            ('session', orm['breakout.SessionAttendance:session']),
            ('status', orm['breakout.SessionAttendance:status']),
            ('arrival_time', orm['breakout.SessionAttendance:arrival_time']),
            ('departure_time', orm['breakout.SessionAttendance:departure_time']),
        ))
        db.send_create_signal('breakout', ['SessionAttendance'])
        
        # Adding model 'Venue'
        db.create_table('breakout_venue', (
            ('id', orm['breakout.Venue:id']),
            ('created_on', orm['breakout.Venue:created_on']),
            ('updated_on', orm['breakout.Venue:updated_on']),
            ('name', orm['breakout.Venue:name']),
            ('slug', orm['breakout.Venue:slug']),
            ('description', orm['breakout.Venue:description']),
            ('street_address_1', orm['breakout.Venue:street_address_1']),
            ('street_address_2', orm['breakout.Venue:street_address_2']),
            ('city', orm['breakout.Venue:city']),
            ('state', orm['breakout.Venue:state']),
            ('zip_code', orm['breakout.Venue:zip_code']),
            ('phone_number', orm['breakout.Venue:phone_number']),
            ('url', orm['breakout.Venue:url']),
            ('image', orm['breakout.Venue:image']),
        ))
        db.send_create_signal('breakout', ['Venue'])
        
        # Adding model 'BreakoutSessionFormat'
        db.create_table('breakout_breakoutsessionformat', (
            ('id', orm['breakout.BreakoutSessionFormat:id']),
            ('created_on', orm['breakout.BreakoutSessionFormat:created_on']),
            ('updated_on', orm['breakout.BreakoutSessionFormat:updated_on']),
            ('name', orm['breakout.BreakoutSessionFormat:name']),
            ('slug', orm['breakout.BreakoutSessionFormat:slug']),
            ('description', orm['breakout.BreakoutSessionFormat:description']),
            ('order', orm['breakout.BreakoutSessionFormat:order']),
        ))
        db.send_create_signal('breakout', ['BreakoutSessionFormat'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'BreakoutSession'
        db.delete_table('breakout_breakoutsession')
        
        # Deleting model 'SessionAttendance'
        db.delete_table('breakout_sessionattendance')
        
        # Deleting model 'Venue'
        db.delete_table('breakout_venue')
        
        # Deleting model 'BreakoutSessionFormat'
        db.delete_table('breakout_breakoutsessionformat')
        
    
    
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
