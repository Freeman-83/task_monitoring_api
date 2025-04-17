from django.urls import include, path

from rest_framework import routers

from tasks.views import TaskViewSet, GroupViewSet

app_name = 'tasks'

router_reports_v1 = routers.DefaultRouter()


router_reports_v1.register(
    'tasks',
    TaskViewSet
)
router_reports_v1.register(
    'groups',
    GroupViewSet
)


urlpatterns = [
    path('', include(router_reports_v1.urls)),
]