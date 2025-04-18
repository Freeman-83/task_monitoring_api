from django.contrib import admin

from .models import Group, Task


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name'
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '---'


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'description',
        'author',
        'group',
        'assignment_date',
        'execution_date',
        'responsible_executor',
        'execution_status'
    )
    search_fields = (
        'title',
        'author',
        'group',
        'assignment_date',
        'execution_date',
        'responsible_executor'
    )
    list_filter = (
        'title',
        'author',
        'group',
        'assignment_date',
        'execution_date',
        'responsible_executor',
        'execution_status'
    )
    empty_value_display = '---'
