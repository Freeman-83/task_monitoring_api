from django.contrib.auth import get_user_model
from django.db import transaction

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from tasks.models import Task, Group
from users.serializers import CustomUserSerializer


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
    responsible_executors = serializers.PrimaryKeyRelatedField(
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
            'responsible_executors',
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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['responsible_executors'] = instance.responsible_executors.values()
        return data

    # @transaction.atomic
    # def create(self, validated_data):
    #     executors_list = validated_data.pop('responsible_executors')

    #     task = Task.objects.create(**validated_data)

    #     task.responsible_executors.set(executors_list)

    #     return task
