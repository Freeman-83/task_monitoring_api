from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'email',
        'chat_id'
    )
    list_display_links = ('username',)
    search_fields = ('username', 'last_name')
    empty_value_display = '---'
