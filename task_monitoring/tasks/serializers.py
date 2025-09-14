from datetime import date

from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from tasks.models import Task, Group

from users.models import ROLE_CHOICES
from users.serializers import CustomUserSerializer, CustomUserContextSerializer


User = get_user_model()


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
        if request_user.is_deputy_director():
            return User.objects.exclude(
                pk=request_user.id,
                role=ROLE_CHOICES[0][0]
            )
        elif request_user.is_head_department():
            return User.objects.filter(
                department=request_user.department
            ).exclude(
                pk=request_user.id
            )
        elif request_user.is_deputy_head_department():
            return User.objects.filter(
                department=request_user.department,
                role=ROLE_CHOICES[4][0]
            ).exclude(
                pk=request_user.id
            )
        return User.objects.all()


class TaskCreateSerializer(serializers.ModelSerializer):
    """Сериализатор Поручения."""

    author = CustomUserSerializer(
        default=serializers.CurrentUserDefault()
    )
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
            'author',
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
                'author',
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
            'application',
            'executions_comment'
        )


class TaskGetSerializer(serializers.ModelSerializer):
    """Контекстный сериализатор Поручения."""

    parent_task = serializers.StringRelatedField()
    redirected_tasks = serializers.StringRelatedField(many=True)
    author = CustomUserContextSerializer(read_only=True)
    executors = CustomUserContextSerializer(
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
            'author',
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
        return all([task.is_completed==False,
                    task.execution_date >= date.today(),
                    task.execution_date <= date.today() + settings.URGENT_EXECUTION_PERIOD])
    
    def get_is_overdue(self, task):
        return all([task.is_completed==False,
                    task.execution_date < date.today()])
