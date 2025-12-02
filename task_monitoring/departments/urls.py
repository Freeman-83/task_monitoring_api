from django.urls import include, path

from rest_framework import routers

from departments.views import EmployeeViewSet, DepartmentViewSet


app_name = 'departments'

router_reports_v1 = routers.DefaultRouter()


router_reports_v1.register(
    'departments',
    DepartmentViewSet
)
router_reports_v1.register(
    'employees',
    EmployeeViewSet
)


urlpatterns = [
    path('', include(router_reports_v1.urls)),
]