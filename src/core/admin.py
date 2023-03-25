from django.contrib import admin
from core.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name']
    search_fields = ['email', 'first_name', 'last_name', 'username']
    list_filter = ['is_staff', 'is_active', 'is_superuser']
    readonly_fields = ['last_login', 'date_joined']
    fieldsets = (
        (
            None, {
                'fields': (
                    'username',
                    'password'
                )
            }
        ),
        (
            'Персональные данные', {
                'fields': (
                    'first_name',
                    'last_name',
                    'email'
                )
            }
        ),
        (
            'Дополнительная информация', {
                'fields': (
                    'last_login',
                    'date_joined'
                )
            }
        )
    )



