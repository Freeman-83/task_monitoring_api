from django.contrib.auth import get_user_model

from djoser import utils
from djoser.views import UserViewSet

from drf_spectacular.utils import extend_schema, extend_schema_view

from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.authtoken.models import Token

from users.serializers import CustomUserSerializer


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

    def get_permissions(self):
        if self.action == 'me':
            self.permission_classes = (permissions.IsAuthenticated,)
        if self.action in ['update', 'partial_update']:
            self.permission_classes = (permissions.IsAdminUser,)
        return super().get_permissions()

    def get_queryset(self):
        queryset = super().get_queryset()
        if (self.action == 'list'
            and not self.request.user.is_staff):
            queryset = queryset.filter(pk=self.request.user.pk)
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.is_staff:
            utils.logout_user(self.request)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


    @action(
        detail=True,
        permission_classes=(permissions.IsAdminUser,)
    )
    def get_user_token(self, request, id):
        current_user = self.queryset.get(pk=id)
        token = Token.objects.get(user=current_user)
        return Response({'Authorization': f'Token {token}'}, status=status.HTTP_200_OK)
