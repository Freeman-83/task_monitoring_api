from django.contrib.auth import get_user_model

from django_filters.rest_framework import (
    FilterSet,
    BooleanFilter,
    ModelMultipleChoiceFilter,
    AllValuesMultipleFilter,
    DateFromToRangeFilter
)

from tasks.models import Task


User = get_user_model()


class TaskFilterSet(FilterSet):

    group = AllValuesMultipleFilter(field_name='group')
    initiator = ModelMultipleChoiceFilter(
        field_name='author__id',
        to_field_name='id',
        label='Инициатор',
        queryset=User.objects.all()
    )
    executors = ModelMultipleChoiceFilter(
        field_name='executors',
        label='Исполнители',
        queryset=User.objects.all()
    )
    assignment_date = DateFromToRangeFilter(
        label='Дата поручения'
    )
    execution_date = DateFromToRangeFilter(
        label='Дата исполнения'
    )
    is_closed = BooleanFilter(
        label='Закрытые'
    )
    is_completed = BooleanFilter(
        label='Исполненные'
    )

    class Meta:
        model = Task
        fields = (
            'group',
            'initiator',
            'executors',
            'assignment_date',
            'execution_date',
            'is_closed',
            'is_completed'
        )
