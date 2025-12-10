from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse # <--- Import this

# --- Simple "Health Check" View ---
def api_root(request):
    return JsonResponse({
        "status": "online",
        "project": "NovaLab API",
        "version": "1.0.0"
    })

urlpatterns = [
    # The Homepage (Fixes the 404)
    path('', api_root), 

    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.accounts.urls')),
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