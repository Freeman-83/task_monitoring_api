from django.contrib.auth import get_user_model

from django_filters.rest_framework import (
    FilterSet,
    BooleanFilter,
    CharFilter,
    ModelMultipleChoiceFilter,
    MultipleChoiceFilter,
    AllValuesMultipleFilter
)

from tasks.models import Task


User = get_user_model()


class TaskFilterSet(FilterSet):

    group = AllValuesMultipleFilter(field_name='group')
    assignment_date = AllValuesMultipleFilter(field_name='assignment_date')
    execution_date = AllValuesMultipleFilter(field_name='execution_date')
    responsible_executors = ModelMultipleChoiceFilter(
        field_name='responsible_executors__last_name',
        to_field_name='name',
        queryset=User.objects.all()
    )
    execution_status = AllValuesMultipleFilter(field_name='execution_status')

    class Meta:
        model = Task
        fields = (
            'group',
            'assignment_date',
            'execution_date',
            'responsible_executors',
            'execution_status'
        )
