from django.contrib import admin
from django.utils.html import format_html

from .models import Topic, Dataset, Task, History


class TopicAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}


class TaskAdmin(admin.ModelAdmin):
    def colored_status(self, obj):
        template = '<span style="background-color:{}; padding: 3px 5px; color: white">{}</span>'
        color = {
            Task.PENDING: "#6c757d ",
            Task.STARTED: "#007bff",
            Task.ERROR: "#dc3545",
            Task.SUCCESS: "#28a745",
        }
        return format_html(template, color.get(obj.status), obj.status)

    colored_status.short_description = "status"
    list_display = ['id', 'task_id', 'colored_status', 'current_state', 'kwargs', 'result']
    list_filter = ['status', 'date_created']


admin.site.register(Topic, TopicAdmin)
admin.site.register(Dataset)
admin.site.register(Task, TaskAdmin)
admin.site.register(History)
