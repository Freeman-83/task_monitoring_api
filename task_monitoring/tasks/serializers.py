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


class TaskSerializer(serializers.ModelSerializer):
    """Сериализатор Задачи."""

    author = CustomUserSerializer(
        default=serializers.CurrentUserDefault()
    )
    
    executors = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True
    )

    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'description',
            'group',
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
    """Контекстный сериализатор Задачи."""

    author = CustomUserContextSerializer(read_only=True)
    executors = CustomUserContextSerializer(
        read_only=True,
        many=True,
    )

    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'description',
            'group',
            'author',
            'executors',
            'assignment_date',
            'execution_date'
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['group'] = instance.group.name
        return data
