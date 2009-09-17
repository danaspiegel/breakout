import datetime

from django.contrib import admin
from django import forms
from django.core.urlresolvers import reverse

from models import *

class VenueAdmin(admin.ModelAdmin):
    fieldsets = ((None, { 'fields': ('name', 'slug', 'description', 'phone_number', 'url', 'image','tags', ) }),
                ('Location', { 'fields': ('street_address_1', 'street_address_2', 'city', 'state', 'zip_code', 'latitude', 'longitude', ) }), )
    prepopulated_fields = { 'slug': ('name', ) }
    list_display_links = ('name', )
    list_display = ('name', 'slug', 'website', 'street_address_1', 'city', 'state', 'zip_code', 'is_geocoded', 'phone_number', )
    search_fields = ['name', 'slug', 'street_address_1', 'city', 'state', 'zip_code', 'phone_number', ]
    save_on_top = True
    actions = ['geocode', ]
    
    def website(self, obj):
        return '<a href="%s" target="_blank">website</a>' % obj.url
    website.allow_tags = True
    website.short_description = 'Website'
    website.admin_order_field = 'url'
    
    def geocode(self, request, queryset):
        geocoded_entries = 0
        for venue in queryset:
            try:
                venue.geocode()
                venue.save()
                geocoded_entries += 1
            except Exception, e:
                self.message_user(request, e)
        self.message_user(request, "%s successfully geocoded." % geocoded_entries)
    geocode.short_description = "Geocode Venues"
    
    def is_geocoded(self, obj):
        return bool(obj.latitude) and bool(obj.longitude)
    is_geocoded.boolean = True
    is_geocoded.short_description = 'Geocoded'

admin.site.register(Venue, VenueAdmin)

class BreakoutCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ('name', ) }
    list_display_links = ('name', )
    list_display = ('order', 'name', 'slug', 'breakout_session_count', 'description', )
    list_editable = ('order', )
    save_on_top = True
    
    def breakout_session_count(self, obj):
        return obj.breakout_sessions.count()
    breakout_session_count.short_description = '# of Sessions'

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
    list_display = ('name', 'venue', 'category', 'start_end_date', 'is_active', 'moderator', 'available_spots', 'registered_users_count', 'lifestream_entries_count')
    list_editable = ( 'category', 'moderator', 'available_spots', )
    search_fields = ['name', 'description', ]
    save_on_top = True
    ordering = ('-start_date', '-end_date', )
    form = BreakoutSessionAdminForm
    
    def is_active(self, obj):
        return obj.is_active
    is_active.boolean = True
    
    def start_end_date(self, obj):
        return "%s-%s" % (obj.start_date.strftime('%a, %b %d %I:%M%p'), obj.end_date.strftime('%I:%M%p'), )
    start_end_date.short_description = 'Event Date'
    
    def registered_users_count(self, obj):
        return obj.registered_users.count()
    registered_users_count.short_description = 'Registrants'

    def lifestream_entries_count(self, obj):
        return obj.lifestream_entries.count()
    lifestream_entries_count.short_description = 'Entries'

admin.site.register(BreakoutSession, BreakoutSessionAdmin)
