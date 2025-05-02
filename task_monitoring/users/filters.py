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


class CustomUserFilterSet(FilterSet):

    department = AllValuesMultipleFilter(field_name='department')
    role = AllValuesMultipleFilter(field_name='role')
    tasks = ModelMultipleChoiceFilter(
        field_name='tasks__execution_status',
        to_field_name='execution_status',
        queryset=Task.objects.all()
    )

    class Meta:
        model = Task
        fields = (
            'department',
            'role',
            'tasks'
        )
