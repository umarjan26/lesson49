from django.contrib import admin

# Register your models here.
from webapp.models import Task, Status, Type, Project


class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'summary', 'status', 'description']
    list_display_links = ['summary']
    list_filter = ['summary', 'type']
    search_fields = ['summary']
    fields = ['summary', 'status', 'type', 'description', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'add_at', 'end_at']
    list_display_links = ['name']
    list_filter = ['name']
    search_fields = ['name']
    fields = ['name',  'description', 'add_at', 'end_at']


class StatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['name']
    list_filter = ['name']
    search_fields = ['name']
    fields = ['name', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']


class TypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['name']
    list_filter = ['name']
    search_fields = ['name']
    fields = ['name', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']


admin.site.register(Status, StatusAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Project, ProjectAdmin)