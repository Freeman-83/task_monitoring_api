from datetime import date

from django.conf import settings
from django.contrib import admin

from .models import Group, Task


class StatusListFilter(admin.SimpleListFilter):
    """Кастомный фильтр статуса поручения."""
    
    title = 'Статус исполнения'
    parameter_name = 'execution_status'

    def lookups(self, request, model_admin):
        return [
            ('on_execution', 'На исполнении'),
            ('urgent', 'Срочные'),
            ('overdue', 'Просроченные'),
            ('completed', 'Исполненные'),
            ('outgoing', 'Исходящие'),
            ('incoming', 'Входящие'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'on_execution':
            return queryset.filter(is_completed=False)
        if self.value() == 'completed':
            return queryset.filter(is_completed=True)
        if self.value() == 'urgent':
            return queryset.filter(
                is_completed=False,
                execution_date__gte=date.today(),
                execution_date__lte=date.today() + settings.URGENT_EXECUTION_PERIOD,
            )
        if self.value() == 'overdue':
            return queryset.filter(
                is_completed=False,
                execution_date__lt=date.today()
            )
        if self.value() == 'outgoing':
            return queryset.filter(
                author=self.request.user
            )
        if self.value() == 'incoming':
            return queryset.filter(
                executors__id=self.request.user.id
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


class RedirectedTasksAdmin(admin.TabularInline):
    model = Task
    min_num = 1
    verbose_name_plural = 'Перенаправленные поручения'


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'group',
        'title',
        'number',
        'parent_task',
        'resolution',
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
        StatusListFilter,
    )
    list_display_links = ('title',)
    empty_value_display = '---'

    inlines = [RedirectedTasksAdmin,]
