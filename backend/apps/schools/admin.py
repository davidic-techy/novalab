from django.contrib import admin
from .models import School, Classroom

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'domain', 'is_active', 'created_at')
    search_fields = ('name', 'slug', 'domain')
    prepopulated_fields = {'slug': ('name',)} # Auto-fill slug as you type name

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('name', 'school', 'grade_level')
    list_filter = ('school',)