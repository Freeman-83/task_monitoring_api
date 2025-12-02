from django.contrib.auth import get_user_model

from djoser.serializers import UserSerializer, UserCreateSerializer

from rest_framework import serializers


User = get_user_model()


class RegisterUserSerializer(UserCreateSerializer):
    """Кастомный сериализатор для регистрации пользователя."""

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'last_name',
            'first_name',
            'second_name',
            'password'
        )

    def validate_email(self, value):
        """Проверка, что указанный адрес эл. почты не занят."""

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "На этот адрес эл. почты уже зарегистрирован аккаунт."
            )
        return value


class CustomUserSerializer(UserSerializer):
    """Кастомный сериализатор Пользователя."""

    initiator_tasks_count = serializers.SerializerMethodField()
    execution_tasks_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'last_name',
            'first_name',
            'second_name'
        )
