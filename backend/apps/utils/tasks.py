from celery import shared_task
from django.core.management import call_command
from django.utils import timezone
from datetime import timedelta

@shared_task
def clear_expired_sessions():
    """
    Cleans up Django session table to remove stale logins.
    """
    call_command('clearsessions')
    return "Expired sessions cleared."

@shared_task
def cleanup_temp_files():
    """
    Example: Delete files in 'temp/' folder older than 24 hours.
    (Implementation depends on specific storage needs).
    """
    # Logic to list and delete files would go here.
    return "Temp files cleanup routine finished."