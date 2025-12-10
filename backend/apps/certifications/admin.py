from django.contrib import admin
from .models import Badge, UserBadge, Certificate

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'xp_value', 'icon')
    search_fields = ('name',)

@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ('user', 'badge', 'earned_at')
    list_filter = ('badge',)
    search_fields = ('user__email', 'user__first_name')

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'course', 'issued_at')
    list_filter = ('course', 'issued_at')
    search_fields = ('user__email', 'course__title', 'id')
    readonly_fields = ('id', 'issued_at') # Prevent tampering with issue datesv