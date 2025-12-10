from .models import SandboxSession, Simulation
from .sandbox.validators import CodeValidator
from django.utils import timezone

class LabService:
    @staticmethod
    def start_session(user, simulation_id):
        """
        Get existing session or create a new one with initial config.
        """
        simulation = Simulation.objects.get(id=simulation_id)
        session, created = SandboxSession.objects.get_or_create(
            user=user,
            simulation=simulation,
            defaults={'code_snapshot': simulation.initial_code}
        )
        return session

    @staticmethod
    def save_progress(session, code):
        """
        Validates and saves the student's work.
        """
        # 1. Run Security Check
        if session.simulation.lab_type == Simulation.LabType.PYTHON_SCRIPT:
            is_safe, message = CodeValidator.validate_python(code)
            if not is_safe:
                raise ValueError(message)

        # 2. Save
        session.code_snapshot = code
        session.updated_at = timezone.now()
        session.save()
        return session