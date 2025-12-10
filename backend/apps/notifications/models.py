from django.db import models
from django.conf import settings

class Notification(models.Model):
    """
    In-App Notifications shown to the user in the Dashboard UI.
    """
    class Type(models.TextChoices):
        INFO = "INFO", "Information"
        SUCCESS = "SUCCESS", "Success"
        WARNING = "WARNING", "Warning"
        ERROR = "ERROR", "Error"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=Type.choices, default=Type.INFO)
    
    # Link to relevant resource (e.g., /projects/123)
    action_url = models.CharField(max_length=500, blank=True, null=True)
    
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} - {self.title}"

class DeliveryLog(models.Model):
    """
    Audit log for Emails and SMS sent out via workers.
    """
    class Channel(models.TextChoices):
        EMAIL = "EMAIL", "Email"
        SMS = "SMS", "SMS"

    recipient = models.CharField(max_length=255)
    channel = models.CharField(max_length=10, choices=Channel.choices)
    subject = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=50, default="SENT") # SENT, FAILED
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)