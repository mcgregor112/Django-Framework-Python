from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ['username', 'email', 'role', 'is_staff', 'is_active']
    search_fields = ['username', 'email']
    list_filter = ['role', 'is_staff', 'is_active']

    # Removing filter_horizontal and fieldsets for groups and user_permissions
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'role', 'is_staff', 'is_active')}),
    )

    add_fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'role', 'is_staff', 'is_active')}),
    )

admin.site.register(User, UserAdmin)
