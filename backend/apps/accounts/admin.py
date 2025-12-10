from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from .models import User

# --- 1. Custom Form to Allow "No Password" Creation ---
class NoPasswordUserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'role', 'school')

    def save(self, commit=True):
        # Create user with an unusable password (since they use Google)
        user = super().save(commit=False)
        user.set_unusable_password()
        if commit:
            user.save()
        return user

# --- 2. Admin Configuration ---
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Use our custom form for adding users
    add_form = NoPasswordUserCreationForm
    
    list_display = ('email', 'first_name', 'last_name', 'role', 'school', 'is_staff')
    list_filter = ('role', 'school', 'is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name', 'username')
    ordering = ('email',)

    # Auto-fill username from email
    prepopulated_fields = {'username': ('email',)}

    # Edit User Page
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'avatar', 'bio')}),
        ('NovaLab Settings', {'fields': ('role', 'school')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Add User Page (Now uses the fields from our Custom Form)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'role', 'school'),
        }),
    )