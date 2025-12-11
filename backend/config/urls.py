from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

# --- Simple "Health Check" View ---
def api_root(request):
    return JsonResponse({
        "status": "online",
        "project": "NovaLab API",
        "version": "1.0.0"
    })

urlpatterns = [
    # 1. The Homepage
    path('', api_root), 

    # 2. Admin
    path('admin/', admin.site.urls),

    # 3. Authentication 
    
    path('auth/', include('apps.accounts.urls')), 
    # standard API path just in case:
    path('api/auth/', include('apps.accounts.urls')),

    # 4. Other API Endpoints
    path('api/', include('apps.schools.urls')),
    path('api/learn/', include('apps.courses.urls')),
    path('api/labs/', include('apps.labs.urls')),
    path('api/projects/', include('apps.projects.urls')),
    path('api/analytics/', include('apps.analytics.urls')),
    path('api/certifications/', include('apps.certifications.urls')),
    path('api/notifications/', include('apps.notifications.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)