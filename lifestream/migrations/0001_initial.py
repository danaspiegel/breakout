
from south.db import db
from django.db import models
from lifestream.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'LifestreamEntry'
        db.create_table('lifestream_lifestreamentry', (
            ('id', orm['lifestream.LifestreamEntry:id']),
            ('created_on', orm['lifestream.LifestreamEntry:created_on']),
            ('updated_on', orm['lifestream.LifestreamEntry:updated_on']),
            ('user', orm['lifestream.LifestreamEntry:user']),
            ('breakout_session', orm['lifestream.LifestreamEntry:breakout_session']),
        ))
        db.send_create_signal('lifestream', ['LifestreamEntry'])
        
        # Adding model 'TwitterUser'
        db.create_table('lifestream_twitteruser', (
            ('id', orm['lifestream.TwitterUser:id']),
            ('created_on', orm['lifestream.TwitterUser:created_on']),
            ('updated_on', orm['lifestream.TwitterUser:updated_on']),
            ('twitter_id', orm['lifestream.TwitterUser:twitter_id']),
            ('screen_name', orm['lifestream.TwitterUser:screen_name']),
            ('url', orm['lifestream.TwitterUser:url']),
            ('profile_image_url', orm['lifestream.TwitterUser:profile_image_url']),
            ('location', orm['lifestream.TwitterUser:location']),
            ('description', orm['lifestream.TwitterUser:description']),
            ('is_muted', orm['lifestream.TwitterUser:is_muted']),
        ))
        db.send_create_signal('lifestream', ['TwitterUser'])
        
        # Adding model 'TwitterStatus'
        db.create_table('lifestream_twitterstatus', (
            ('lifestreamentry_ptr', orm['lifestream.TwitterStatus:lifestreamentry_ptr']),
            ('twitter_id', orm['lifestream.TwitterStatus:twitter_id']),
            ('twitter_user', orm['lifestream.TwitterStatus:twitter_user']),
            ('text', orm['lifestream.TwitterStatus:text']),
            ('location', orm['lifestream.TwitterStatus:location']),
        ))
        db.send_create_signal('lifestream', ['TwitterStatus'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'LifestreamEntry'
        db.delete_table('lifestream_lifestreamentry')
        
        # Deleting model 'TwitterUser'
        db.delete_table('lifestream_twitteruser')
        
        # Deleting model 'TwitterStatus'
        db.delete_table('lifestream_twitterstatus')
        
    
    
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
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'breakout_sessions'", 'to': "orm['breakout.BreakoutSessionFormat']"}),
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
        },
        'lifestream.lifestreamentry': {
            'breakout_session': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'lifestream_entries'", 'to': "orm['breakout.BreakoutSession']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'lifestream_entries'", 'to': "orm['auth.User']"})
        },
        'lifestream.twitterstatus': {
            'lifestreamentry_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['lifestream.LifestreamEntry']", 'unique': 'True', 'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'twitter_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'twitter_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'twitter_statuses'", 'to': "orm['lifestream.TwitterUser']"})
        },
        'lifestream.twitteruser': {
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_muted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'profile_image_url': ('django.db.models.fields.URLField', [], {'max_length': '400'}),
            'screen_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True'}),
            'twitter_id': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'})
        }
    }
    
    complete_apps = ['lifestream']
