from django.db import models
from django.conf import settings
import uuid

class Simulation(models.Model):
    """
    Defines a specific Virtual Lab scenario.
    e.g., "Traffic Light Controller" or "Sentiment Analysis Model Builder".
    """
    class LabType(models.TextChoices):
        PYTHON_SCRIPT = "PYTHON", "Python Scripting"
        BLOCKLY = "BLOCKLY", "Visual Blocks"
        AI_MODEL = "AI_MODEL", "AI Model Configurator"
        CIRCUIT_SIM = "CIRCUIT", "Circuit Simulator"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    lab_type = models.CharField(max_length=20, choices=LabType.choices)
    
    # The "Hardware" Config.
    # e.g., for a Circuit: {"components": ["led_red", "battery"], "target_voltage": 5}
    # e.g., for AI: {"dataset_url": "/static/data/traffic.csv", "allowed_models": ["LinearRegression"]}
    environment_config = models.JSONField(default=dict, blank=True)
    
    # Starter code provided to the student
    initial_code = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class SandboxSession(models.Model):
    """
    Tracks a student's active work on a simulation.
    """
    class Status(models.TextChoices):
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        COMPLETED = "COMPLETED", "Completed"
        FAILED = "FAILED", "Failed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="lab_sessions")
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE)
    
    # The student's current code or block configuration
    code_snapshot = models.TextField(blank=True)
    
    # The output log of their last run
    last_output = models.TextField(blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.IN_PROGRESS)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'simulation') # One active session per lab per user

    def __str__(self):
        return f"{self.user.email} - {self.simulation.title}"