from django.contrib import admin
from django.contrib.auth import get_user_model

from departments.models import Employee, Department


User = get_user_model()


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'curator'
    )
    list_display_links = ('name',)
    search_fields = ('name',)
    empty_value_display = '---'


@admin.register(Employee)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'department',
        'role'
    )
    list_display_links = ('user',)
    search_fields = ('department', 'role')
    list_filter = ('department', 'role')
    empty_value_display = '---'
