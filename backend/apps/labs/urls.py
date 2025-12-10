from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import SimulationViewSet, WorkspaceViewSet

router = DefaultRouter()
router.register(r'simulations', SimulationViewSet, basename='simulation')
router.register(r'workspace', WorkspaceViewSet, basename='workspace')

urlpatterns = [
    path('', include(router.urls)),
]