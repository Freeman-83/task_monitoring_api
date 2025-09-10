from datetime import date

from django.conf import settings
from django.contrib.auth import get_user_model

from django_filters.rest_framework import (
    FilterSet,
    BooleanFilter,
    ModelMultipleChoiceFilter,
    AllValuesMultipleFilter
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
    is_urgent = BooleanFilter(
        method='get_is_urgent'
    )
    is_overdue = BooleanFilter(
        method='get_is_overdue'
    )
    is_outgoing = BooleanFilter(
        method='get_is_outgoing'
    )
    is_incoming = BooleanFilter(
        method='get_is_incoming'
    )

    class Meta:
        model = Task
        fields = (
            'group',
            'executors',
            'is_completed_by_author',
            'is_completed_by_executor'
        )

    def get_is_urgent(self, queryset, name, value):
        return queryset.filter(
            is_completed=False,
            execution_date__gte=date.today(),
            execution_date__lte=date.today() + settings.URGENT_EXECUTION_PERIOD,
        )

    def get_is_overdue(self, queryset, name, value):
        return queryset.filter(
            is_completed=False,
            execution_date__lt=date.today()
        )
    
    def get_is_outgoing(self, queryset, name, value):
        return queryset.filter(
            author=self.request.user
        )
    
    def get_is_incoming(self, queryset, name, value):
        return queryset.filter(
            executors__id=self.request.user.id,
        )
