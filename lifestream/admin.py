from django.contrib import admin
from django.core import urlresolvers

from models import *

class TwitterUserAdmin(admin.ModelAdmin):
    list_display_links = ('twitter_id', )
    list_display = ('twitter_id', 'twitter_name', 'image', 'location', 'tweet_count', 'updated_on',)
    # list_editable = ('location', )
    search_fields = ['screen_name', ]
    
    def image(self, obj):
        if obj.profile_image_url:
            return '<a href="%s">image</a>' % (obj.profile_image_url, )
        else:
            return ''
    image.allow_tags = True
    image.short_description = 'Profile Image'
    image.admin_order_field = 'profile_image_url'
    
    def twitter_name(self, obj):
        return '<a href="http://twitter.com/%s/">@%s</a>' % (obj.screen_name, obj.screen_name, )
    twitter_name.allow_tags = True
    twitter_name.short_description = 'Screen Name'
    twitter_name.admin_order_field = 'screen_name'

admin.site.register(TwitterUser, TwitterUserAdmin)

class TwitterStatusAdmin(admin.ModelAdmin):
    list_display = ('twitter_id', 'breakout_session_name', 'screen_name', 'text', 'location', 'created_on', )
    search_fields = ['twitter_id', 'user__screen_name', 'text', ]
    
    def screen_name(self, obj):
        return '<a href="%s">%s</a>' % (urlresolvers.reverse('admin:lifestream_twitteruser_change', args=(obj.twitter_user.id,)), obj.twitter_user.screen_name, )
    screen_name.allow_tags = True
    screen_name.short_description = 'Twitter User'
    screen_name.admin_order_field = 'user__screen_name'
    
    def breakout_session_name(self, obj):
        return '<a href="%s">%s</a>' % (urlresolvers.reverse('admin:breakout_breakoutsession_change', args=(obj.breakout_session.id,)), obj.breakout_session.name, )
    breakout_session_name.allow_tags = True
    breakout_session_name.short_description = 'Breakout Session'
    breakout_session_name.admin_order_field = 'breakout_session__name'

admin.site.register(TwitterStatus, TwitterStatusAdmin)

class FlickrImageAdmin(admin.ModelAdmin):
    list_display = ('url', )

admin.site.register(FlickrImage, FlickrImageAdmin)
