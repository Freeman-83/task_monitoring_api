from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Sum
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.utils import extend_schema, extend_schema_view

from rest_framework import (
    filters,
    mixins,
    permissions,
    status,
    views,
    viewsets
)

from tasks.models import Group, Task

from tasks.serializers import GroupSerializer, TaskSerializer

from tasks.filters import TaskFilterSet

from tasks.permissions import IsAdminOrExecutor


User = get_user_model()


@extend_schema(tags=['Тип задач'])
@extend_schema_view(
    list=extend_schema(summary='Получение списка типов задач'),
    create=extend_schema(summary='Создание нового типа задач'),
    retrieve=extend_schema(summary='Получение типа задачи')
)
class GroupViewSet(viewsets.ModelViewSet):
    """Вьюсет Типа задач."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes=(permissions.IsAdminUser,)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    ordering_fields = ['name',]


@extend_schema(tags=['Общий отчет по предобработке'])
@extend_schema_view(
    list=extend_schema(summary='Получение всех задач'),
    create=extend_schema(summary='Создание задачи'),
    retrieve=extend_schema(summary='Получение задачи'),
)
class TaskViewSet(viewsets.ModelViewSet):
    """Вьюсет Задачи."""

    queryset = Task.objects.select_related(
        'group'
    ).order_by(
        'execution_date'
    ).all()
    serializer_class = TaskSerializer
    permission_classes=(IsAdminOrExecutor,)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = TaskFilterSet
    ordering_fields = ['assignment_date',]

    def get_queryset(self):
        if self.action == 'list' and not self.request.user.is_staff:
            return Task.objects.filter(
                responsible_executor=self.request.user
            ).select_related(
                'group'
            ).order_by(
                'execution_date'
            ).all()
        return super().get_queryset()
