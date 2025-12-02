from django.contrib import admin
from django.contrib.auth import get_user_model


User = get_user_model()


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'first_name',
        'second_name',
        'last_name'
    )
    list_display_links = ('email',)
    search_fields = ('email', 'last_name')
    empty_value_display = '---'
