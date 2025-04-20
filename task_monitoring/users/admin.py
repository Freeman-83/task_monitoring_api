from django.contrib import admin

from .models import CustomUser, Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name'
    )
    list_display_links = ('name',)
    search_fields = ('name',)
    empty_value_display = '---'


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'first_name',
        'last_name',
        'department',
        'chat_id'
    )
    list_display_links = ('email',)
    search_fields = ('email', 'last_name')
    empty_value_display = '---'
