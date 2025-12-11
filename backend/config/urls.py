from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

def api_root(request):
    return JsonResponse({
        "status": "online",
        "project": "NovaLab API",
        "version": "1.0.0"
    })

urlpatterns = [
    path('', api_root),
    path('admin/', admin.site.urls),

    
    path('auth/', include('apps.accounts.urls')),
    path('schools/', include('apps.schools.urls')),
    path('learn/', include('apps.courses.urls')),
    path('labs/', include('apps.labs.urls')),
    path('projects/', include('apps.projects.urls')),
    path('analytics/', include('apps.analytics.urls')),
    path('certifications/', include('apps.certifications.urls')),
    path('notifications/', include('apps.notifications.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)