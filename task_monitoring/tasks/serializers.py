from datetime import date

from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from tasks.models import Task, Group

from departments.models import Employee, ROLE_CHOICES
from departments.serializers import (
    EmployeeCreateSerializer,
    EmployeeGetSerializer,
    EmployeeContextSerializer,
    DepartmentSerializer
)
# from users.serializers import CustomUserSerializer, CustomUserContextSerializer


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор Типа задачи."""

    class Meta:
        model = Group
        fields = (
            'id',
            'name',
            'tasks'
        )


class ExecutorsField(serializers.PrimaryKeyRelatedField):
    """Кастомное поле выбора исполнителя Поручения."""

    def get_queryset(self):
        request_user = self.context['request'].user
        if request_user.employee.is_director():
            return Employee.objects.exclude(
                pk=request_user.employee.id,
                role=ROLE_CHOICES[0][0]
            )
        elif request_user.employee.is_head_department():
            return Employee.objects.filter(
                department=request_user.employee.department
            ).exclude(
                pk=request_user.employee.id
            )
        elif request_user.employee.is_deputy_head_department():
            return Employee.objects.filter(
                department=request_user.employee.department,
                role=ROLE_CHOICES[4][0]
            ).exclude(
                pk=request_user.employee.id
            )
        return Employee.objects.all()


class TaskCreateSerializer(serializers.ModelSerializer):
    """Сериализатор Поручения."""

    # initiator = serializers.PrimaryKeyRelatedField(
    #     default=serializers.CurrentUserDefault
    # )

    executors = ExecutorsField(many=True)

    class Meta:
        model = Task
        fields = (
            'id',
            'group',
            'title',
            'number',
            'parent_task',
            'resolution',
            'initiator',
            'executors',
            'assignment_date',
            'execution_date'
        )

    validators = [
        UniqueTogetherValidator(
            queryset=Task.objects.all(),
            fields=[
                'title',
                'number',
                'initiator',
                'assignment_date'
            ]
        )
    ]

    def validate(self, data):
        if data['execution_date'] < date.today():
            raise serializers.ValidationError('Некорректная дата исполнения поручения!')
        return data
    

class TaskExecutorUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор изменения Поручения для исполнителя."""

    class Meta:
        model = Task
        fields = (
            'id',
            'is_completed',
            'executions_application',
            'executions_comment'
        )


class TaskGetSerializer(serializers.ModelSerializer):
    """Контекстный сериализатор Поручения."""

    parent_task = serializers.StringRelatedField()
    redirected_tasks = serializers.StringRelatedField(many=True)
    initiator = EmployeeContextSerializer(read_only=True)
    executors = EmployeeContextSerializer(
        read_only=True,
        many=True,
    )
    is_urgent = serializers.SerializerMethodField()
    is_overdue = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = (
            'id',
            'group',
            'title',
            'number',
            'assignment_date',
            'execution_date',
            'parent_task',
            'redirected_tasks',
            'resolution',
            'initiator',
            'executors',
            'is_closed',
            'is_completed',
            'is_urgent',
            'is_overdue',
            'executions_comment'
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['group'] = instance.group.name
        return data

    def get_is_urgent(self, task):
        return all(
            [task.is_completed==False,
             task.execution_date >= date.today(),
             task.execution_date <= date.today() + settings.URGENT_EXECUTION_PERIOD]
        )
    
    def get_is_overdue(self, task):
        return all(
            [task.is_completed==False,
             task.execution_date < date.today()]
        )
