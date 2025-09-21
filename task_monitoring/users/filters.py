from django.contrib.auth import get_user_model

from django_filters.rest_framework import (
    FilterSet,
    ModelMultipleChoiceFilter,
    AllValuesMultipleFilter
)

from tasks.models import Task
from users.models import Department


User = get_user_model()


class CustomUserFilterSet(FilterSet):

    department = ModelMultipleChoiceFilter(
        field_name='department__name',
        to_field_name='name',
        queryset=Department.objects.all()
    )
    role = AllValuesMultipleFilter(field_name='role')
    execution_tasks = ModelMultipleChoiceFilter(
        field_name='execution_tasks',
        to_field_name='title',
        queryset=Task.objects.all()
    )

    class Meta:
        model = Task
        fields = (
            'department',
            'role',
            'execution_tasks'
        )
