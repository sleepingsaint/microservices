from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as userAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

# Register your models here.
class CustomUserAdmin(userAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ('email', 'username', 'is_staff', 'is_active', 'last_login')
    list_filter = ('is_staff', 'is_active', 'last_login')
    
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'bio')}),
        (_('Permissions'), {
            'fields': ('is_private', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active', "is_private")}
        ),
    )

    search_fields = ('email', 'username')
    ordering = ('email', 'username', 'last_login')

admin.site.register(CustomUser, CustomUserAdmin)