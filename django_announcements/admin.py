
from django.contrib import admin

from models import Announcement
from forms import AnnouncementAdminForm

class AnnouncementAdmin(admin.ModelAdmin):
    # list_display = ("title", "creator", "creation_date", "members_only")
    list_display = ("title", "creation_date", "members_only")
    list_filter = ("members_only",)
    form = AnnouncementAdminForm

admin.site.register(Announcement, AnnouncementAdmin)
