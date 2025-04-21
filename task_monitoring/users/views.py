from rest_framework import permissions, viewsets
from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema, extend_schema_view

from djoser.conf import settings
from djoser.views import UserViewSet

from users.models import CustomUser

from users.serializers import CustomUserSerializer

from tasks.permissions import IsAdminOrExecutor


@extend_schema(tags=['Пользователи'])
@extend_schema_view(
    list=extend_schema(summary='Получение списка пользователей'),
    create=extend_schema(summary='Создание нового пользователя'),
    retrieve=extend_schema(summary='Получение данных пользователя'),
    update=extend_schema(summary='Изменение данных пользователя'),
    partial_update=extend_schema(summary='Частичное изменение данных данных пользователя'),
    destroy=extend_schema(summary='Удаление данных пользователя'),
)
class CustomUserViewSet(UserViewSet):
    """Кастомный вьюсет для пользователей."""

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.IsAdminUser,)

    def get_queryset(self):
        if self.action == 'list' and not self.request.user.is_staff:
            return CustomUser.objects.filter(pk=self.request.user.id)
        return super().get_queryset()

    def get_permissions(self):
        if self.action == 'me':
            self.permission_classes = (permissions.IsAuthenticated,)
        return super().get_permissions()
