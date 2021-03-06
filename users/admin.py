from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = (
        'email', 'is_staff', 'is_active',
    )
    list_filter = ('email', 'is_staff', 'is_active',)

    fieldsets = (
        (None, {'fields': (
            'user_image','first_name', 'last_name','email', 'password'
        )}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'user_image', 'first_name', 'last_name',
                'password1', 'password2', 'is_staff', 'is_active'
            )}
        ),
    )

    search_fields = ('email',)
    ordering = ('id',)

admin.site.register(CustomUser, CustomUserAdmin)
