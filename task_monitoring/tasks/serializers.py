from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from tasks.models import Task, Group
from users.serializers import CustomUserSerializer


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

    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'description',
            'author',
            'group',
            'assignment_date',
            'execution_date',
            'responsible_executor'
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
