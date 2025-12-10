from django.contrib import admin
from .models import Simulation, SandboxSession

@admin.register(Simulation)
class SimulationAdmin(admin.ModelAdmin):
    list_display = ('title', 'lab_type', 'slug', 'created_at')
    list_filter = ('lab_type',)
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)} # Auto-type the slug

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'lab_type')
        }),
        ('Technical Config', {
            'fields': ('initial_code', 'environment_config'),
            'description': 'JSON config for the environment and starter code for the student.'
        }),
    )

@admin.register(SandboxSession)
class SandboxSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'simulation', 'status', 'updated_at')
    list_filter = ('status', 'simulation')
    search_fields = ('user__email', 'simulation__title')
    readonly_fields = ('updated_at',) # Keep history safe