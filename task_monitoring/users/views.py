from rest_framework import permissions, viewsets

from drf_spectacular.utils import extend_schema, extend_schema_view

from djoser.views import UserViewSet

from users.models import CustomUser

from users.serializers import CustomUserSerializer

# from api.permissions import UserPermission


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

    def get_permissions(self):
        if self.action == 'me':
            self.permission_classes = (permissions.IsAuthenticated,)
        return super().get_permissions()