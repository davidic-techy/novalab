from django.db import models
from django.conf import settings
import uuid

class ProjectTemplate(models.Model):
    """
    The blueprint for a project (e.g., "Build a Weather App").
    """
    class Difficulty(models.TextChoices):
        BEGINNER = "BEGINNER", "Beginner"
        INTERMEDIATE = "INTERMEDIATE", "Intermediate"
        ADVANCED = "ADVANCED", "Advanced"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    difficulty = models.CharField(max_length=20, choices=Difficulty.choices)
    
    # JSON definition of the starter files.
    # e.g. { "main.py": "print('Start here')", "requirements.txt": "pandas" }
    scaffold_config = models.JSONField(default=dict)
    
    # Grading Rubric config (e.g. required keywords, passing unit tests)
    grading_config = models.JSONField(default=dict)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Project(models.Model):
    """
    A student's specific instance of a project.
    """
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        SUBMITTED = "SUBMITTED", "Submitted"
        GRADED = "GRADED", "Graded"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="projects")
    template = models.ForeignKey(ProjectTemplate, on_delete=models.CASCADE)
    
    # The actual code files created by the student
    # Stored as JSON: { "main.py": "...", "utils.py": "..." }
    artifact_data = models.JSONField(default=dict)
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    
    # Grading results
    grade_score = models.FloatField(null=True, blank=True)
    feedback = models.TextField(blank=True)
    
    submitted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'template') # Student can only have one active instance per template

    def __str__(self):
        return f"{self.template.title} by {self.user.email}"