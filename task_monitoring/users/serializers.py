import re

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

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
            'department',
            'role'
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
            'chat_id',
            'department',
            'role',
            'tasks'
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['department']:
            data['department'] = instance.department.name
        data['tasks'] = instance.tasks.values()

        return data


class CustomUserContextSerializer(serializers.ModelSerializer):
    """Контекстный сериализатор Пользователя."""

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'chat_id',
            'department',
            'role'
        )
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['department']:
            data['department'] = instance.department.name
        return data
