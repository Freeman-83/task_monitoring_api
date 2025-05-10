from django.contrib.auth import get_user_model

from djoser.views import UserViewSet

from drf_spectacular.utils import extend_schema, extend_schema_view

from rest_framework import permissions, viewsets

from users.models import Department

from users.serializers import CustomUserSerializer, DepartmentSerializer


User = get_user_model()


@extend_schema(tags=['Пользователи'])
@extend_schema_view(
    list=extend_schema(summary='Список пользователей'),
    create=extend_schema(summary='Создание нового пользователя'),
    retrieve=extend_schema(summary='Данные пользователя'),
    update=extend_schema(summary='Изменение данных пользователя'),
    partial_update=extend_schema(summary='Частичное изменение данных данных пользователя'),
    destroy=extend_schema(summary='Удаление данных пользователя'),
)
class CustomUserViewSet(UserViewSet):
    """Кастомный вьюсет для пользователей."""

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.IsAdminUser,)

    def get_queryset(self):
        if self.action == 'list' and not self.request.user.is_staff:
            return User.objects.filter(pk=self.request.user.id)
        return super().get_queryset()

    def get_permissions(self):
        if self.action == 'me':
            self.permission_classes = (permissions.IsAuthenticated,)
        return super().get_permissions()


@extend_schema(tags=['Подразделения'])
@extend_schema_view(
    list=extend_schema(summary='Получение списка подразделений'),
    create=extend_schema(summary='Создание нового подразделения'),
    retrieve=extend_schema(summary='Получение данных подразделения'),
    update=extend_schema(summary='Изменение данных подразделения'),
    partial_update=extend_schema(summary='Частичное изменение данных данных подразделения'),
    destroy=extend_schema(summary='Удаление данных подразделения'),
)
class DepartmentViewSet(viewsets.ModelViewSet):
    """Вьюсет Подразделения."""

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = (permissions.IsAdminUser,)
