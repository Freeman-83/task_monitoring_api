from datetime import date

from django.conf import settings
from django.contrib.auth import get_user_model

from django_filters.rest_framework import (
    FilterSet,
    BooleanFilter,
    CharFilter,
    ModelMultipleChoiceFilter,
    MultipleChoiceFilter,
    AllValuesMultipleFilter,
    ChoiceFilter
)

from tasks.models import Task


User = get_user_model()

CHOICES = [
    ('on_execution', 'on_execution'),
    ('urgent', 'urgent'), 
    ('overdue', 'overdue'), 
    ('completed', 'overdue')
]


class TaskFilterSet(FilterSet):

    group = AllValuesMultipleFilter(field_name='group')
    executors = ModelMultipleChoiceFilter(
        field_name='executors__id',
        to_field_name='id',
        queryset=User.objects.all()
    )
    
    is_urgent = BooleanFilter(
        field_name='is_urgent',
        method='get_execution_status'
    )
    is_overdue = BooleanFilter(
        field_name='is_overdue',
        method='get_execution_status'
    )

    class Meta:
        model = Task
        fields = (
            'group',
            'executors',
            'is_completed'
        )

    def get_execution_status(self, queryset, name, value):
        if name == 'is_urgent' and value:
            return queryset.filter(
                is_completed=False,
                execution_date__gte=date.today(),
                execution_date__lte=date.today() + settings.EXECUTION_REMINDER_PERIOD,
            )
        if name == 'is_overdue' and value:
            return queryset.filter(
                is_completed=False,
                execution_date__lt=date.today()
            )
        return queryset.all()
