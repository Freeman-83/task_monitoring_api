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
    author = ModelMultipleChoiceFilter(
        field_name='author__last_name',
        to_field_name='last_name',
        queryset=User.objects.all()
    )
    is_on_execution = BooleanFilter(
        field_name='is_completed',
        method='get_is_on_execution'
    )
    is_outgoing = BooleanFilter(
        method='get_is_outgoing'
    )
    is_urgent = BooleanFilter(
        method='get_is_urgent'
    )
    is_overdue = BooleanFilter(
        method='get_is_overdue'
    )
    is_completed = BooleanFilter(
        field_name='is_completed',
        method='get_is_completed'
    )
    is_closed = BooleanFilter(
        field_name='is_closed',
        method='get_is_closed'
    )

    class Meta:
        model = Task
        fields = (
            'group',
            'is_closed',
            'is_completed'
        )

    def get_is_on_execution(self, queryset, name, value):
        return queryset.filter(
            executors__id=self.request.user.id,
            is_completed=False
        )
    
    def get_is_outgoing(self, queryset, name, value):
        return queryset.filter(author=self.request.user.id)

    def get_is_urgent(self, queryset, name, value):
        return queryset.filter(
            executors__id=self.request.user.id,
            is_completed=False,
            execution_date__gte=date.today(),
            execution_date__lte=date.today() + settings.URGENT_EXECUTION_PERIOD,
        )

    def get_is_overdue(self, queryset, name, value):
        return queryset.filter(
            executors__id=self.request.user.id,
            is_completed=False,
            execution_date__lt=date.today()
        )

    def get_is_completed(self, queryset, name, value):
        return queryset.filter(
            executors__id=self.request.user.id,
            is_completed=True
        )

    def get_is_closed(self, queryset, name, value):
        return queryset.filter(
            author=self.request.user,
            is_closed=True
        )
