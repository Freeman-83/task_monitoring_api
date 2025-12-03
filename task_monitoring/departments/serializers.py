from rest_framework import serializers

from departments.models import Department, Employee
from users.serializers import CustomUserSerializer


class EmployeeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания профиля Сотрудника."""

    class Meta:
        model = Employee
        fields = (
            'user',
            'department',
            'role'
        )
    

class EmployeeGetSerializer(serializers.ModelSerializer):
    """Сериализатор профиля Сотрудника."""

    user = CustomUserSerializer(read_only=True)
    initiator_tasks_count = serializers.SerializerMethodField()
    execution_tasks_count = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = (
            'user',
            'department',
            'role',
            'initiator_tasks',
            'execution_tasks',
            'initiator_tasks_count',
            'execution_tasks_count'
        )

    def get_initiator_tasks_count(self, employee):
        return employee.initiator_tasks.count()
    
    def get_execution_tasks_count(self, employee):
        return employee.execution_tasks.count()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['department']:
            data['department'] = instance.department.name
        data['initiator_tasks'] = []
        for task in instance.initiator_tasks.all():
            data['initiator_tasks'].append(
                {
                    'group': task.group.name,
                    'title': task.title,
                    'number': task.number,
                    'assignment_date': task.assignment_date,
                    'execution_date': task.execution_date,
                    'is_closed': task.is_closed,
                    'is_completed': task.is_completed
                }
            )
        data['execution_tasks'] = []
        for task in instance.execution_tasks.all():
            data['execution_tasks'].append(
                {
                    'group': task.group.name,
                    'title': task.title,
                    'number': task.number,
                    'initiator': f'{task.initiator.user.last_name} {task.initiator.user.first_name}',
                    'assignment_date': task.assignment_date,
                    'execution_date': task.execution_date,
                    'is_closed': task.is_closed,
                    'is_completed': task.is_completed
                }
            )

        return data


class EmployeeContextSerializer(serializers.ModelSerializer):
    """Контекстный сериализатор Сотрудника."""

    user = serializers.StringRelatedField()
    department = serializers.StringRelatedField()
    role = serializers.StringRelatedField()

    class Meta:
        model = Employee
        fields = (
            'user',
            'department',
            'role'
        )


class DepartmentSerializer(serializers.ModelSerializer):
    """Кастомный сериализатор Подразделения."""

    employees = EmployeeContextSerializer(
        read_only=True,
        many=True
    )

    class Meta:
        model = Department
        fields = (
            'id',
            'name',
            'curator',
            'employees'
        )
