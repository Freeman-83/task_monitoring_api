from datetime import date

from django.conf import settings
from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.utils import extend_schema, extend_schema_view

from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework import (
    filters,
    permissions,
    status,
    viewsets
)

from tasks.models import Group, Task

from tasks.serializers import (
    GroupSerializer,
    TaskCreateSerializer,
    TaskGetSerializer,
    TaskExecutorUpdateSerializer
)

from tasks.filters import TaskFilterSet

from tasks.permissions import IsAdminOrManagerOrReadOnly

from users.models import ROLE_CHOICES


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


@extend_schema(tags=['Поручения'])
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
    serializer_class = TaskCreateSerializer
    permission_classes=(IsAdminOrManagerOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = TaskFilterSet
    ordering_fields = ('execution_date',)

    def get_queryset(self):
        if not self.request.user.is_staff and not self.request.user.is_director():

            if (self.request.user.is_deputy_director()
                or self.request.user.is_head_department()
                or self.request.user.is_deputy_head_department()):

                if self.action in ['update', 'partial_update', 'delete']:
                    queryset = Task.objects.filter(
                        author=self.request.user.id
                    ).select_related(
                        'group'
                    ).prefetch_related(
                        'executors'
                    ).all()

                    return queryset

                if self.action in ['list', 'retrieve']:
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
    

    @extend_schema(summary='Поручения на исполнении')
    @action(
        detail=False,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def on_execution_tasks(self, request):
        tasks = Task.objects.filter(
            executors__id=request.user.id,
            is_completed=False
        )
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    @extend_schema(summary='Исходящие поручения')
    @action(
        detail=False,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def outgoing_tasks(self, request):
        tasks = Task.objects.filter(
            author=request.user.id,
            is_completed=False,
            is_closed=False
        )
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    @extend_schema(summary='Поручения на закрытие')
    @action(
        detail=False,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def on_close_tasks(self, request):
        tasks = Task.objects.filter(
            author=request.user.id,
            is_completed=True,
            is_closed=False
        )
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @extend_schema(summary='Перенаправление поручения')
    @action(
        methods=['POST'],
        detail=True,
        permission_classes=(IsAdminOrManagerOrReadOnly,)
    )
    def redirect_task(self, request, pk):
        if request.user.is_staff or request.user.is_director():
            current_task = get_object_or_404(Task, pk=pk)
        else:
            current_task = get_object_or_404(
                Task,
                pk=pk,
                executors__id=request.user.id,
                is_closed=False,
                execution_date__gt=date.today() + settings.URGENT_EXECUTION_PERIOD
            )

        request_data = {
            'title': current_task.title,
            'group': current_task.group.id,
            'parent_task': current_task.id,
            'resolution': request.data.get('resolution', current_task.resolution),
            'executors': request.data.get('executors'),
            'execution_date': request.data.get('execution_date', current_task.execution_date)
        }

        serializer = self.get_serializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

    @extend_schema(summary='Отметка об исполнении поручения исполнителем')
    @action(
        methods=['PATCH'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,),
        serializer_class=TaskExecutorUpdateSerializer
    )
    def complete_task(self, request, pk):
        if request.user.is_staff or request.user.is_director():
            current_task = get_object_or_404(
                Task,
                pk=pk,
                is_completed=False
            )
        else:
            current_task = get_object_or_404(
                Task,
                pk=pk,
                executors__id=request.user.id,
                is_completed=False
            )

        request_data = {
            'is_completed': True,
            'application': request.data.get('application'),
            'executions_comment': request.data.get('executions_comment')
        }

        serializer = self.get_serializer(
            current_task,
            data=request_data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @extend_schema(summary='Отметка об исполнении поручения инициатором')
    @action(
        methods=['PATCH'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,),
        serializer_class=TaskGetSerializer
    )
    def close_task(self, request, pk):
        if request.user.is_staff or request.user.is_director():
            current_task = get_object_or_404(Task, pk=pk)
        else:
            current_task = get_object_or_404(
                Task,
                pk=pk,
                author=request.user.id,
                is_completed=True
            )

        current_task.is_closed = True
        current_task.save()

        serializer = self.get_serializer(current_task)

        return Response(serializer.data, status=status.HTTP_200_OK)
