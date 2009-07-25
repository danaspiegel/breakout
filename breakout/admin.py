from django.contrib import admin
from django.core.urlresolvers import reverse

from models import *

class VenueAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ('name', ) }
    list_display_links = ('name', )
    list_display = ('name', 'slug', 'website', 'street_address_1', 'city', 'state', 'zip_code', 'phone_number', )
    search_fields = ['name', 'slug', 'street_address_1', 'city', 'state', 'zip_code', 'phone_number', ]
    
    def website(self, obj):
        return '<a href="%s" target="_blank">website</a>' % obj.url
    website.allow_tags = True
    website.short_description = 'Website'
    website.admin_order_field = 'url'

admin.site.register(Venue, VenueAdmin)

class BreakoutCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ('name', ) }
    list_display_links = ('name', )
    list_display = ('order', 'name', 'slug', 'session_count', 'description', )
    list_editable = ('order', )
    
    def session_count(self, obj):
        return obj.breakout_sessions.count()
    session_count.short_description = '# of Sessions'

admin.site.register(BreakoutCategory, BreakoutCategoryAdmin)

class SessionAttendanceInline(admin.TabularInline):
    model = SessionAttendance
    extra = 3

class BreakoutSessionAdmin(admin.ModelAdmin):
    list_display_links = ('name', )
    inlines = (SessionAttendanceInline, )
    list_filter = ('category', )
    list_display = ('name', 'is_active', 'venue', 'category', 'start_date', 'end_date', 'moderator', 'available_spots', 'registered_users_count')
    list_editable = ( 'venue', 'category', 'start_date', 'end_date', 'moderator', 'available_spots', )
    search_fields = ['name', 'description', ]
    
    def registered_users_count(self, obj):
        return obj.registered_users.count()
    registered_users_count.short_description = '# of Sessions'

admin.site.register(BreakoutSession, BreakoutSessionAdmin)
