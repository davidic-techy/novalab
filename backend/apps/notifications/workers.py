import contextlib
from celery import shared_task
from .email import EmailService
from .sms import SMSService
from .models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()

@shared_task
def send_email_async(user_id, subject, template_name, context):
    """
    Task to send email in background.
    """
    with contextlib.suppress(User.DoesNotExist):
        user = User.objects.get(id=user_id)
        EmailService.send_email(user.email, subject, template_name, context)

@shared_task
def send_system_notification(user_id, title, message, type="INFO"):
    """
    Creates an In-App notification (Bell Icon).
    """
    with contextlib.suppress(User.DoesNotExist):
        user = User.objects.get(id=user_id)
        Notification.objects.create(
            user=user,
            title=title,
            message=message,
            notification_type=type
        )