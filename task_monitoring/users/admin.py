from django.contrib import admin
from django.contrib.auth import get_user_model

from users.models import Department


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


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'first_name',
        'second_name',
        'last_name',
        'department',
        'role'
    )
    list_display_links = ('email',)
    search_fields = ('email', 'last_name')
    list_filter = ('department', 'role')
    empty_value_display = '---'
