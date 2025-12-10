from django.contrib import admin
from .models import ProjectTemplate, Project

@admin.register(ProjectTemplate)
class ProjectTemplateAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty', 'created_at')
    list_filter = ('difficulty',)
    search_fields = ('title', 'description')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    # Columns to show
    list_display = ('id', 'user', 'template', 'status', 'grade_score', 'submitted_at')
    
    # Filters on the right side
    list_filter = ('status', 'template')
    
    # Search bar
    search_fields = ('user__email', 'template__title')
    
    # --- THIS IS THE MAGIC LINE ---
    # Allows you to change status directly in the list view
    list_editable = ('status', 'grade_score')