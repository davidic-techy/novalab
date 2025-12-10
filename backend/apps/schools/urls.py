from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SchoolViewSet, ClassroomViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'schools', SchoolViewSet, basename='school')
router.register(r'classrooms', ClassroomViewSet, basename='classroom')

# The API URLs are determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]