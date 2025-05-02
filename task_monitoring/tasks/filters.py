from django.contrib.auth import get_user_model

from django_filters.rest_framework import (
    FilterSet,
    BooleanFilter,
    CharFilter,
    ModelMultipleChoiceFilter,
    MultipleChoiceFilter,
    AllValuesMultipleFilter,
)

from tasks.models import Task


User = get_user_model()


class TaskFilterSet(FilterSet):

    group = AllValuesMultipleFilter(field_name='group')
    executors = ModelMultipleChoiceFilter(
        field_name='executors__id',
        to_field_name='id',
        queryset=User.objects.all()
    )
    # execution_status = AllValuesMultipleFilter(field_name='execution_status')

    class Meta:
        model = Task
        fields = (
            'group',
            'executors',
            'is_completed'
        )
