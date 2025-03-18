from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser , Book

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Specify fields to display in the list view
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')

    # Specify fields for filtering in the admin
    list_filter = ('role', 'is_staff', 'is_active')

    # Specify which fields can be edited in the admin form
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role',)}),
    )

    # Specify fields for add user form
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('role',)}),
    )

class BookAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('title', 'author')
    
    # Add search functionality to search by title or author
    search_fields = ('title', 'author')
    
    # Add ordering to make the list sorted by title by default
    ordering = ('title',)
    
admin.site.register(Book, BookAdmin)