from datetime import timedelta, date, datetime

from django.contrib.auth import get_user_model
from django.db import transaction

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from tasks.models import Task, Group
from users.serializers import CustomUserSerializer, CustomUserContextSerializer


User = get_user_model()


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор Типа задачи."""

    class Meta:
        model = Group
        fields = (
            'id',
            'name'
        )


class ExecutorsField(serializers.PrimaryKeyRelatedField):
    """Кастомное поле выбора исполнителя Задачи."""

    def get_queryset(self):
        request_user = self.context['request'].user
        subordinate_departments = request_user.subordinate_departments.all()
        if request_user.is_staff or request_user.is_director():
            return User.objects.all()
        elif request_user.is_head_department():
            return User.objects.filter(department=request_user.department).all()
        return User.objects.filter(department__in=subordinate_departments).all()


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
            'description',
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
                'group',
                'assignment_date'
            ]
        )
    ]


class TaskGetSerializer(serializers.ModelSerializer):
    """Контекстный сериализатор Поручения."""

    author = CustomUserContextSerializer(read_only=True)
    executors = CustomUserContextSerializer(
        read_only=True,
        many=True,
    )

    class Meta:
        model = Task
        fields = (
            'id',
            'group',
            'title',
            'number',
            'parent_task',
            'redirected_tasks',
            'description',
            'author',
            'executors',
            'assignment_date',
            'execution_date',
            'execution_status'
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['group'] = instance.group.name
        return data
