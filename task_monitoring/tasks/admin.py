from datetime import date

from django.conf import settings
from django.contrib import admin

from .models import Group, Task


class StatusListFilter(admin.SimpleListFilter):
    """Кастомный фильтр для статуса исполнения поручения."""
    
    title = 'Статус исполнения'
    parameter_name = 'status'

    def lookups(self, request, model_admin):

        return [
            ('on_execution', 'На исполнении'),
            ('is_urgent_task', 'Срочные'),
            ('is_overdue_task', 'Просроченные'),
            ('completed', 'Исполненные')
        ]

    def queryset(self, request, queryset):

        if self.value() == 'on_execution':
            return queryset.filter(
                is_completed=False,
            )
        if self.value() == 'is_urgent_task':
            return queryset.filter(
                execution_date__gte=date.today(),
                execution_date__lte=date.today() + settings.EXECUTION_REMINDER_PERIOD,
            )
        if self.value() == 'is_overdue_task':
            return queryset.filter(
                execution_date__lt=date.today(),
            )
        if self.value() == 'completed':
            return queryset.filter(
                is_completed=True,
            )


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
        'group',
        'title',
        'number',
        'parent_task',
        'description',
        'author',
        'assignment_date',
        'execution_date',
        'tasks_file',
        'is_completed'
    )
    search_fields = (
        'title',
        'assignment_date',
        'number',
        'author',
        'group',
        'execution_date',
    )
    list_filter = (
        'title',
        'author',
        'group',
        'assignment_date',
        'execution_date',
        # 'is_completed',
        StatusListFilter,
    )
    list_display_links = ('title',)
    empty_value_display = '---'

    # @admin.display(description='Срочное', empty_value='')
    # def is_urgent_task(self, task):
    #     if not task.is_completed:
    #         return all([date.today() < task.execution_date,
    #             date.today() >= task.execution_date - settings.EXECUTION_REMINDER_PERIOD])

    # @admin.display(description='Просроченное', empty_value='')
    # def is_overdue_task(self, task):
    #     if not task.is_completed and date.today() > task.execution_date:
    #         return '!!!'
