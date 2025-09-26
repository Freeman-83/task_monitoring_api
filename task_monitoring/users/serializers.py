from django.contrib.auth import get_user_model

from djoser.serializers import UserSerializer, UserCreateSerializer

from rest_framework import serializers

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
            'second_name',
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


class CustomUserSerializer(UserSerializer):
    """Кастомный сериализатор Пользователя."""

    initiator_tasks_count = serializers.SerializerMethodField()
    execution_tasks_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'second_name',
            'last_name',
            'department',
            'role',
            'initiator_tasks_count',
            'execution_tasks_count',
            'initiator_tasks',
            'execution_tasks'
        )

    def get_initiator_tasks_count(self, user):
        return user.initiator_tasks.count()
    
    def get_execution_tasks_count(self, user):
        return user.execution_tasks.count()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['department']:
            data['department'] = instance.department.name
        data['initiator_tasks'] = []
        for task in instance.initiator_tasks.all():
            data['initiator_tasks'].append(
                {
                    'group': task.group.name,
                    'title': task.title,
                    'number': task.number,
                    'assignment_date': task.assignment_date,
                    'execution_date': task.execution_date,
                    'is_closed': task.is_closed,
                    'is_completed': task.is_completed
                }
            )
        data['execution_tasks'] = []
        for task in instance.execution_tasks.all():
            data['execution_tasks'].append(
                {
                    'group': task.group.name,
                    'title': task.title,
                    'number': task.number,
                    'initiator': f'{task.initiator.last_name} {task.initiator.first_name}',
                    'assignment_date': task.assignment_date,
                    'execution_date': task.execution_date,
                    'is_closed': task.is_closed,
                    'is_completed': task.is_completed
                }
            )

        return data


class CustomUserContextSerializer(serializers.ModelSerializer):
    """Контекстный сериализатор Пользователя."""

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'second_name',
            'last_name',
            'email',
            'department',
            'role'
        )
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['department']:
            data['department'] = instance.department.name
        return data


class DepartmentSerializer(serializers.ModelSerializer):
    """Кастомный сериализатор Подразделения."""

    employees = CustomUserContextSerializer(
        read_only=True,
        many=True
    )

    class Meta:
        model = Department
        fields = (
            'id',
            'name',
            'curator',
            'employees'
        )
