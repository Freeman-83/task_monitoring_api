from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'first_name',
        'last_name',
        'chat_id'
    )
    list_display_links = ('email',)
    search_fields = ('email', 'last_name')
    empty_value_display = '---'
