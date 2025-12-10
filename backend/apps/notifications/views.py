from rest_framework import viewsets, decorators, response, status, permissions
from .models import Notification
from .serializers import NotificationSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    """
    Manage In-App Notifications.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    @decorators.action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """
        POST /api/notifications/{id}/mark_read/
        """
        notif = self.get_object()
        notif.is_read = True
        notif.save()
        return response.Response({"status": "read"})

    @decorators.action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """
        POST /api/notifications/mark_all_read/
        """
        self.get_queryset().update(is_read=True)
        return response.Response({"status": "all read"})