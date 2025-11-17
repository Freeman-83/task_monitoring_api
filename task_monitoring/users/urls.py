from django.urls import include, path

from rest_framework import routers

from users.views import CustomUserViewSet, DepartmentViewSet


app_name = 'users'

router_users_v1 = routers.DefaultRouter()

router_users_v1.register(
    'users',
    CustomUserViewSet,
    basename='users'
)
router_users_v1.register(
    'departments',
    DepartmentViewSet,
    basename='departments'
)

urlpatterns = [
    path('', include(router_users_v1.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt')),
]