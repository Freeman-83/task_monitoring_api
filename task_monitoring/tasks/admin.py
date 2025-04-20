from django.contrib import admin

from .models import Group, Task, TaskUser


class TaskToUser(admin.TabularInline):
    model = TaskUser
    min_num = 1


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
        # 'responsible_executors',
        'execution_status'
    )
    search_fields = (
        'title',
        'author',
        'group',
        'assignment_date',
        'execution_date',
        # 'responsible_executors'
    )
    list_filter = (
        'title',
        'author',
        'group',
        'assignment_date',
        'execution_date',
        # 'responsible_executors',
        'execution_status'
    )
    empty_value_display = '---'

    inlines = [TaskToUser,]


@admin.register(TaskUser)
class TaskUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'user')
    search_fields = ('task', 'user')
    list_filter = ('task', 'user')
    empty_value_display = '-пусто-'
