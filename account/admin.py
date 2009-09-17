from django.contrib import admin
from django.core.urlresolvers import reverse
from django.contrib.sessions.models import Session

from models import *

class SessionAdmin(admin.ModelAdmin):
    list_display = ('delete_session', 'session_key', 'user', 'expire_date', )
    list_display_links = ('session_key', )
    
    def delete_session(self, obj):
        return '<a href="/admin/sessions/session/%s/delete/">delete</a>' % (obj.pk, )
    delete_session.allow_tags = True
    delete_session.short_description = ''
    
    def user(self, obj):
        data = obj.get_decoded()
        uid = data.get('_auth_user_id', None)
        if uid is None:
            return ''
        else:
            user = User.objects.get(pk=uid)
            return '<a href="/admin/auth/user/%s/">%s</a>' % (user.pk, user.username)
    user.allow_tags = True
    user.short_description = 'User'

admin.site.register(Session, SessionAdmin)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'age', 'gender', 'twitter_user', 'twitter_access_token', )
    list_filter = ('age', 'gender', )

admin.site.register(UserProfile, UserProfileAdmin)
