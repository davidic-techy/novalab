from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CertificateViewSet, MyBadgesViewSet

router = DefaultRouter()
router.register(r'certificates', CertificateViewSet, basename='certificate')
router.register(r'badges', MyBadgesViewSet, basename='badge')

urlpatterns = [
    path('', include(router.urls)),
]