from rest_framework import serializers
from .models import Event, DailyStats

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['event_type', 'metadata'] # Only what the frontend sends

class DailyStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyStats
        fields = ['date', 'total_logins', 'active_students', 'lessons_completed', 'labs_run']