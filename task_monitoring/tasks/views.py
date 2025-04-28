
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

from rest_framework import (
    filters,
    mixins,
    permissions,
    status,
    views,
    viewsets
)

from tasks.models import Group, Task

from tasks.serializers import GroupSerializer, TaskSerializer, TaskGetSerializer

from tasks.filters import TaskFilterSet

from tasks.permissions import IsAdminOrManagerOrReadOnly


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

    # def create()


    # @extend_schema(summary='Удаление отчетов за определенный период')
    # @action(
    #     methods=['POST'],
    #     detail=False,
    #     permission_classes=[permissions.AllowAny]
    # )
    # def clear_report_period(self, request):
    #     message, result = delete_report(request.data, self.queryset)
    #     status_data = {
    #         'not_found_error': status.HTTP_404_NOT_FOUND,
    #         'report_period_error': status.HTTP_400_BAD_REQUEST,
    #         'success_status': status.HTTP_204_NO_CONTENT
    #     }

    #     return Response(data=message, status=status_data[result])

