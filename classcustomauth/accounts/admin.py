from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User
# Register your models here.

class UserModelAdmin(UserAdmin):
    model = User
    list_display = ['id', 'name', 'email', 'is_active', 'is_staff', 'is_superuser', 'is_customer', 'is_seller']
    list_filter = ['is_superuser']

    fieldsets = [
        ('User Credentials', {'fields': ['email', 'password']}),
        ('Personal Info', {'fields': ['name', 'city']}),
        ('Permissions', {'fields': ['is_active', 'is_staff', 'is_superuser', 'is_customer', 'is_seller']}),
    ]

    add_fieldsets = [
        (
            None, 
            { 
                'classes':['wide'], 
                'fields': ['email', 'password1', 'password2']
                
            }
        )
    ]

    search_fields = ['email']
    ordering = ['email', 'id']
    filter_horizontal = []

admin.site.register(User, UserModelAdmin)
