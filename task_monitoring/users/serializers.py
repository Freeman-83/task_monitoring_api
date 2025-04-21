import re

from django.contrib.auth import get_user_model

from djoser.serializers import UserSerializer, UserCreateSerializer

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Department


User = get_user_model()


class RegisterUserSerializer(UserCreateSerializer):
    """Кастомный сериализатор для регистрации пользователя."""

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'password',
            'department'
        )

    def validate_email(self, value):
        """Проверка, что указанный адрес эл. почты не занят."""

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "На этот адрес эл. почты уже зарегистрирован аккаунт."
            )
        return value


class DepartmentSerializer(serializers.ModelSerializer):
    """Кастомный сериализатор Подразделения."""

    class Meta:
        model = Department
        fields = (
            'id',
            'name',
            'users'
        )


class CustomUserSerializer(UserSerializer):
    """Кастомный сериализатор Пользователя."""

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'department',
            'chat_id',
            'tasks'
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['department']:
            data['department'] = instance.department.name
        
        res = []
        for task in instance.tasks.values():
            res.append(
                {'Название': task['title'],
                 # 'Тип поручения': task['group'],
                 'Дата поручения': task['assignment_date'],
                 'Дата исполнения': task['execution_date'],
                 'Статус': task['execution_status']}
            )
        data['tasks'] = res
        return data


class CustomUserContextSerializer(serializers.ModelSerializer):
    """Контекстный сериализатор Пользователя."""

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'department'
        )
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['department']:
            data['department'] = instance.department.name
        return data
