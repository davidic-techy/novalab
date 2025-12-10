from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectTemplateViewSet, ProjectViewSet

router = DefaultRouter()
router.register(r'templates', ProjectTemplateViewSet, basename='project-template')
router.register(r'my-projects', ProjectViewSet, basename='my-project')

urlpatterns = [
    path('', include(router.urls)),
]