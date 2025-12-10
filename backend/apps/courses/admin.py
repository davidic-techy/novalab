from django.contrib import admin
from .models import Course, Module, Lesson, Question

# --- INLINES (Nested Editing) ---

class QuestionInline(admin.StackedInline):
    """
    Allows adding Questions directly inside the Lesson page.
    """
    model = Question
    extra = 1 # Show 1 empty slot by default

class LessonInline(admin.StackedInline):
    """
    Allows adding Lessons directly inside the Module page.
    """
    model = Lesson
    extra = 0
    fields = ('title', 'type', 'order', 'duration_minutes')

class ModuleInline(admin.StackedInline):
    """
    Allows adding Modules directly inside the Course page.
    """
    model = Module
    extra = 0
    fields = ('title', 'order')

# --- ADMIN PAGES ---

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'school', 'instructor', 'is_published', 'created_at')
    list_filter = ('is_published', 'school')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)} # Auto-fill slug
    inlines = [ModuleInline] # Edit modules here

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    search_fields = ('title', 'course__title')
    inlines = [LessonInline] # Edit lessons here

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'type', 'duration_minutes', 'order')
    list_filter = ('type', 'module__course')
    search_fields = ('title', 'module__title')
    inlines = [QuestionInline]
    
    fieldsets = (
        (None, {
            # FIX: Removed 'slug' from this list
            'fields': ('module', 'title', 'type', 'order', 'duration_minutes')
        }),
        ('Content Configuration', {
            'fields': ('content',),
            'description': 'Enter JSON config here. For Video: {"video_url": "..."}. For Text: {"text": "..."}'
        }),
    )
    