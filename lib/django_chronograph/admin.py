import datetime
from dateutil.relativedelta import *
from django.contrib import admin
from django.utils.translation import ungettext, ugettext_lazy as _
from django.http import HttpResponseRedirect, Http404
from django.conf.urls.defaults import patterns, url
from models import Job, Log

class JobAdmin(admin.ModelAdmin):
    list_display = ('name', 'next_run', 'last_run', 'frequency', 'params', 'get_timeuntil', 'is_running')
    list_filter = ('frequency', 'disabled',)
    actions = ['set_not_running', ]
    
    fieldsets = (
        (None, {
            'fields': ('name', ('command', 'args',), 'disabled',)
        }),
        ('Frequency options', {
            'classes': ('wide',),
            'fields': ('frequency', 'next_run', 'params',)
        }),
    )
    
    def set_not_running(self, request, queryset):
        for job in queryset:
            job.is_running = False
            job.save()
        self.message_user(request, 'The selected job(s) have been reset')
    set_not_running.short_description = "Reset Job Execution Status"
    
    def run_job_view(self, request, pk):
        """
        Runs the specified job.
        """
        try:
            job = Job.objects.get(pk=pk)
        except Job.DoesNotExist:
            raise Http404
        job.run(save=False)
        request.user.message_set.create(message=_('The job "%(job)s" was run successfully.') % {'job': job})        
        return HttpResponseRedirect(request.path + "../")
    
    def get_urls(self):
        urls = super(JobAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'^(.+)/run/$', self.admin_site.admin_view(self.run_job_view), name="chronograph_job_run")
        )
        return my_urls + urls

class LogAdmin(admin.ModelAdmin):
    list_display = ('job_name', 'run_date',)
    search_fields = ('stdout', 'stderr', 'job__name', 'job__command')
    date_hierarchy = 'run_date'
    actions = ['delete_old_logs', ]
    
    def delete_old_logs(self, request, queryset):
        print "DELETING!"
        two_weeks_ago = datetime.datetime.utcnow() - relativedelta(weeks=2)
        deleted_count = 0
        for log in Log.objects.filter(run_date__lte=two_weeks_ago):
            log.delete()
            deleted_count += 1
        self.message_user(request, '%s logs older than 2 weeks have been deleted' % deleted_count)
    delete_old_logs.short_description = "Delete logs older than 2 weeks"
    
    def job_name(self, obj):
      return obj.job.name
    job_name.short_description = _(u'Name')

admin.site.register(Job, JobAdmin)
admin.site.register(Log, LogAdmin)