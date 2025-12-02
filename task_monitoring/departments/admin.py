from django.contrib import admin

from departments.models import Employee, Department


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
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'department',
        'role'
    )
    list_display_links = ('user',)
    search_fields = ('department', 'role')
    list_filter = ('department', 'role')
    empty_value_display = '---'
