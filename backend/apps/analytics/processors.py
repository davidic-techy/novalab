from django.db.models import Count
from django.utils import timezone
from .models import Event, DailyStats
# FIX: Import School from the correct app
from apps.schools.models import School 

class AnalyticsProcessor:
    """
    Aggregates raw Event logs into DailyStats.
    """
    
    @staticmethod
    def aggregate_school_stats(school_id=None):
        today = timezone.now().date()
        
        # Filter scope
        schools = School.objects.all()
        if school_id:
            schools = schools.filter(id=school_id)
            
        for school in schools:
            # Get events for today
            todays_events = Event.objects.filter(
                school=school, 
                timestamp__date=today
            )

            # Calculate Metrics
            logins = todays_events.filter(event_type=Event.EventType.LOGIN).count()
            lessons = todays_events.filter(event_type=Event.EventType.LESSON_COMPLETE).count()
            labs = todays_events.filter(event_type=Event.EventType.LAB_START).count()
            
            # Count unique users active today
            active_users = todays_events.values('user').distinct().count()

            # Update or Create Stats Record
            DailyStats.objects.update_or_create(
                date=today,
                school=school,
                defaults={
                    'total_logins': logins,
                    'lessons_completed': lessons,
                    'labs_run': labs,
                    'active_students': active_users
                }
            )