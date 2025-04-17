from django_filters.rest_framework import (
    FilterSet,
    BooleanFilter,
    CharFilter,
    ModelMultipleChoiceFilter,
    MultipleChoiceFilter,
    AllValuesMultipleFilter
)

from tasks.models import Task


class TaskFilterSet(FilterSet):

    group = AllValuesMultipleFilter(field_name='group')
    assignment_date = AllValuesMultipleFilter(field_name='assignment_date')
    execution_date = AllValuesMultipleFilter(field_name='execution_date')
    responsible_executor = AllValuesMultipleFilter(field_name='responsible_executor')

    class Meta:
        model = Task
        fields = (
            'group',
            'assignment_date',
            'execution_date',
            'responsible_executor'
        )