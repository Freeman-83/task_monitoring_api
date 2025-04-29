from datetime import date

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Sum
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.utils import extend_schema, extend_schema_view

from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework import (
    filters,
    mixins,
    permissions,
    status,
    views,
    viewsets
)

from tasks.models import Group, Task, EXECUTION_STATUS

from tasks.serializers import GroupSerializer, TaskSerializer, TaskGetSerializer

from tasks.filters import TaskFilterSet

from tasks.permissions import IsAdminOrManagerOrReadOnly


User = get_user_model()


@extend_schema(tags=['Тип задач'])
@extend_schema_view(
    list=extend_schema(summary='Список типов поручений'),
    create=extend_schema(summary='Создание нового типа поручения'),
    retrieve=extend_schema(summary='Тип поручения'),
    update=extend_schema(summary='Изменение типа поручения'),
    partial_update=extend_schema(summary='Частичное изменение типа поручения'),
    destroy=extend_schema(summary='Удаление типа поручения'),
)
class GroupViewSet(viewsets.ModelViewSet):
    """Вьюсет Типа поручения."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes=(permissions.IsAdminUser,)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    ordering_fields = ['name',]


@extend_schema(tags=['Общий отчет по предобработке'])
@extend_schema_view(
    list=extend_schema(summary='Список поручений'),
    create=extend_schema(summary='Создание нового поручения'),
    retrieve=extend_schema(summary='Поручение'),
    update=extend_schema(summary='Изменение поручения'),
    partial_update=extend_schema(summary='Частичное изменение поручения'),
    destroy=extend_schema(summary='Удаление поручения'),
)
class TaskViewSet(viewsets.ModelViewSet):
    """Вьюсет Поручения."""

    queryset = Task.objects.select_related(
        'group'
    ).prefetch_related(
        'executors'
    ).order_by(
        'execution_date'
    ).all()
    serializer_class = TaskSerializer
    permission_classes=(IsAdminOrManagerOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = TaskFilterSet
    ordering_fields = ['execution_date',]

    def get_queryset(self):
        if self.action in ['list', 'retrieve'] and not self.request.user.is_staff:
            if self.request.user.is_director():
                authors_queryset = Task.objects.filter(
                    author=self.request.user.id
                ).select_related(
                    'group'
                ).prefetch_related(
                    'executors'
                ).order_by(
                    'execution_date'
                ).all()

                return authors_queryset

            elif self.request.user.is_deputy_director() or self.request.user.is_head_department():
                authors_queryset = Task.objects.filter(
                    author=self.request.user.id
                ).select_related(
                    'group'
                ).prefetch_related(
                    'executors'
                ).order_by(
                    'execution_date'
                ).all()

                executors_queryset = Task.objects.filter(
                    executors__id=self.request.user.id
                ).select_related(
                    'group'
                ).prefetch_related(
                    'executors'
                ).order_by(
                    'execution_date'
                ).all()

                result_queryset = authors_queryset | executors_queryset

                return result_queryset

            else:
                executors_queryset = Task.objects.filter(
                    executors__id=self.request.user.id
                ).select_related(
                    'group'
                ).prefetch_related(
                    'executors'
                ).order_by(
                    'execution_date'
                ).all()

                return executors_queryset

        return super().get_queryset()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TaskGetSerializer
        return super().get_serializer_class()


    @extend_schema(summary='Актуализация статусов поручений')
    @action(
        methods=['PATCH'],
        detail=False,
        permission_classes=[permissions.IsAdminUser]
    )
    def update_tasks(self, request):
        tasks = self.queryset.filter(
            execution_status__in=[EXECUTION_STATUS[1][0], EXECUTION_STATUS[2][0]]
        )
        for task in tasks:
            if (date.today() < task.execution_date
                and date.today() >= task.execution_date - settings.EXECUTION_REMINDER_PERIOD):
                task.execution_status = EXECUTION_STATUS[2][0]
            elif date.today() > task.execution_date:
                task.execution_status = EXECUTION_STATUS[3][0]

            task.save()

        serializer = self.get_serializer(tasks, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
