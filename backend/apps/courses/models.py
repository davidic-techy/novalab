from django.db import models
from django.conf import settings
from apps.schools.models import School

class Course(models.Model):
    """
    A full learning track (e.g., 'Python for Beginners').
    Can be Global (NovaLab content) or School-Specific.
    """
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to="course_thumbnails/", blank=True, null=True)
    
    # If null, it's a global course for everyone. If set, only that school sees it.
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True)
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Module(models.Model):
    """
    A section within a course (e.g., 'Chapter 1: Variables').
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="modules")
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Lesson(models.Model):
    """
    The actual content unit.
    """
    class ContentType(models.TextChoices):
        VIDEO = "VIDEO", "Video"
        TEXT = "TEXT", "Text/Article"
        QUIZ = "QUIZ", "Quiz"
        LAB = "LAB", "Virtual Lab"

    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    type = models.CharField(max_length=20, choices=ContentType.choices, default=ContentType.TEXT)

    # Stores the Video URL, Markdown text, or Lab Config JSON
    content = models.JSONField(default=dict, help_text="Config for Video URL, Text body, or Lab ID")
    
    # Estimated time to complete in minutes
    duration_minutes = models.IntegerField(default=10)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

# --- QUIZ MODELS ---

class Question(models.Model):
    """
    A single question attached to a Lesson (if type=QUIZ).
    """
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()
    
    # Options stored as JSON: {"a": "Blue", "b": "Red", "c": "Green"}
    options = models.JSONField()
    
    # The correct key (e.g., "b")
    correct_answer = models.CharField(max_length=1) 
    
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.text[:50]