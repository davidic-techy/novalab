from django.db import models
from django.conf import settings
from apps.schools.models import School

class Event(models.Model):
    """
    Immutable log of a specific action.
    """
    class EventType(models.TextChoices):
        LOGIN = "LOGIN", "User Login"
        LESSON_COMPLETE = "LESSON_COMPLETE", "Lesson Completed"
        LAB_START = "LAB_START", "Lab Started"
        PROJECT_SUBMIT = "PROJECT_SUBMIT", "Project Submitted"
        PAGE_VIEW = "PAGE_VIEW", "Page View"

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="events")
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="events")
    
    event_type = models.CharField(max_length=50, choices=EventType.choices)
    
    # Flexible generic data (e.g., {"lesson_id": 5, "score": 80})
    metadata = models.JSONField(default=dict, blank=True)
    
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['event_type', 'timestamp']),
            models.Index(fields=['school', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.event_type} by {self.user}"


class DailyStats(models.Model):
    """
    Aggregated stats per school per day. 
    Queries hit this table instead of scanning millions of Event rows.
    """
    date = models.DateField()
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    
    total_logins = models.IntegerField(default=0)
    active_students = models.IntegerField(default=0)
    lessons_completed = models.IntegerField(default=0)
    labs_run = models.IntegerField(default=0)
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('date', 'school')