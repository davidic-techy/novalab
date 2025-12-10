from django.db import models
import uuid

class School(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, help_text="Subdomain e.g. 'kings' in kings.novalab.ai")
    domain = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Classroom(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="classrooms")
    name = models.CharField(max_length=100)
    
    # --- ADD THIS MISSING LINE ---
    grade_level = models.IntegerField(default=1, help_text="1-12 representing grade level") 
    
    def __str__(self):
        return f"{self.name} ({self.school.name})"