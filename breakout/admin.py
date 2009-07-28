import datetime

from django.contrib import admin
from django import forms
from django.core.urlresolvers import reverse

from models import *

class VenueAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ('name', ) }
    list_display_links = ('name', )
    list_display = ('name', 'slug', 'website', 'street_address_1', 'city', 'state', 'zip_code', 'phone_number', )
    search_fields = ['name', 'slug', 'street_address_1', 'city', 'state', 'zip_code', 'phone_number', ]
    save_on_top = True
    
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
    save_on_top = True
    
    def session_count(self, obj):
        return obj.breakout_sessions.count()
    session_count.short_description = '# of Sessions'

admin.site.register(BreakoutCategory, BreakoutCategoryAdmin)

class SessionAttendanceInline(admin.TabularInline):
    model = SessionAttendance
    extra = 3

class BreakoutSessionAdminForm(forms.ModelForm):
    class Meta:
        model = BreakoutSession
    
    def clean_end_date(self):
        # do something that validates your data
        start_date = self.cleaned_data["start_date"]
        end_date = self.cleaned_data["end_date"]
        if (start_date.year == end_date.year) and (start_date.month == end_date.month) and (start_date.day == end_date.day) and start_date < end_date:
            return self.cleaned_data["end_date"]
        raise forms.ValidationError("End date must be on the same day as the start date")

class BreakoutSessionAdmin(admin.ModelAdmin):
    list_display_links = ('name', )
    inlines = (SessionAttendanceInline, )
    list_filter = ('category', )
    list_display = ('name', 'venue', 'category', 'start_end_date', 'is_active', 'moderator', 'available_spots', 'registered_users_count')
    list_editable = ( 'category', 'moderator', 'available_spots', )
    search_fields = ['name', 'description', ]
    save_on_top = True
    ordering = ('-start_date', '-end_date', )
    form = BreakoutSessionAdminForm
    
    def start_end_date(self, obj):
        return "%s-%s" % (obj.start_date.strftime('%a, %b %d %I:%M%p'), obj.end_date.strftime('%I:%M%p'), )
    start_end_date.short_description = 'Event Date'
    
    def registered_users_count(self, obj):
        return obj.registered_users.count()
    registered_users_count.short_description = '# of Registrants'

admin.site.register(BreakoutSession, BreakoutSessionAdmin)
