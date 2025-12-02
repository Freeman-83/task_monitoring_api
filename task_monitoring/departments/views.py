from drf_spectacular.utils import extend_schema, extend_schema_view

from rest_framework import permissions, viewsets

from departments.models import Employee, Department

from departments.serializers import (
    EmployeeCreateSerializer,
    EmployeeGetSerializer,
    DepartmentSerializer
)


@extend_schema(tags=['Подразделения'])
@extend_schema_view(
    list=extend_schema(summary='Получение списка подразделений'),
    create=extend_schema(summary='Создание нового подразделения'),
    retrieve=extend_schema(summary='Получение данных подразделения'),
    update=extend_schema(summary='Изменение данных подразделения'),
    partial_update=extend_schema(summary='Частичное изменение данных данных подразделения'),
    destroy=extend_schema(summary='Удаление данных подразделения'),
)
class DepartmentViewSet(viewsets.ModelViewSet):
    """Вьюсет Подразделения."""

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = (permissions.IsAdminUser,)


@extend_schema(tags=['Сотрудники'])
@extend_schema_view(
    list=extend_schema(summary='Получение списка сотрудников'),
    create=extend_schema(summary='Создание нового сотрудника'),
    retrieve=extend_schema(summary='Получение данных сотрудника'),
    update=extend_schema(summary='Изменение данных сотрудника'),
    partial_update=extend_schema(summary='Частичное изменение данных данных сотрудника'),
    destroy=extend_schema(summary='Удаление данных сотрудника'),
)
class EmployeeViewSet(viewsets.ModelViewSet):
    """Вьюсет Сотрудника организации."""

    queryset = Employee.objects.select_related('user', 'department').all()
    serializer_class = EmployeeCreateSerializer
    permission_classes = (permissions.IsAdminUser,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return EmployeeGetSerializer
        return super().get_serializer_class()
