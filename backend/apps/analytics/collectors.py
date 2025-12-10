from .models import Event

class EventCollector:
    """
    Service responsible for validating and ingesting raw events.
    """
    
    @staticmethod
    def capture(user, event_type, metadata=None):
        """
        Records an event to the database.
        """
        if metadata is None:
            metadata = {}

        # --- FIX: ROBUST SAFETY CHECKS ---
        
        # 1. If user is not logged in, we cannot log a school event
        if not user.is_authenticated:
            return None

        # 2. If user has no school assigned (e.g. Superadmin), skip or handle gracefully
        # Use getattr to avoid crash if 'school' field is missing from User model
        school = getattr(user, 'school', None)
        
        if not school:
            return None

        # ---------------------------------

        try:
            event = Event.objects.create(
                user=user,
                school=school,
                event_type=event_type,
                metadata=metadata
            )
            return event
        except Exception as e:
            # Prevent analytics from crashing the main app
            print(f"Analytics Error: {e}")
            return None