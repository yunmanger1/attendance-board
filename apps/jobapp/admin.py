from django.contrib import admin
from jobapp.models import DailyJob, Job, JobGroup

class DailyJobAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'n', 'pub_date','importance')
    list_filter = ('n','is_on',)
    search_fields = ('title', 'text')
admin.site.register(DailyJob, DailyJobAdmin)

class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'n', 'pub_date', 'importance')
    list_filter = ('n','is_on',)
    search_fields = ('title', 'text')
admin.site.register(Job, JobAdmin)


class JobGroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'pub_date',)
    list_filter = ('is_public',)
    search_fields = ('title', 'text', 'user')
admin.site.register(JobGroup, JobGroupAdmin)
