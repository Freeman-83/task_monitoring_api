import re

from django.contrib.auth import get_user_model

from djoser.serializers import UserSerializer, UserCreateSerializer

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Department


User = get_user_model()


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
            'in_tasks'
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['department']:
            data['department'] = instance.department.name
        return data


class CustomUserContextSerializer(UserSerializer):
    """Кастомный сериализатор Пользователя."""

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'department'
        )


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

    # def validate_username(self, data):
    #     username = data
    #     error_symbols_list = []

    #     for symbol in username:
    #         if not re.search(r'^[\w.@+-]+\Z', symbol):
    #             error_symbols_list.append(symbol)
    #     if error_symbols_list:
    #         raise serializers.ValidationError(
    #             f'Символы {"".join(error_symbols_list)} недопустимы'
    #         )
    #     return data