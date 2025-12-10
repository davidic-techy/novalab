from django.db import models
from django.conf import settings
import uuid

class Badge(models.Model):
    """
    Achievements like 'Python Pioneer' or 'Bug Hunter'.
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.ImageField(upload_to="badges/", help_text="Upload a transparent PNG")
    xp_value = models.IntegerField(default=50)
    
    def __str__(self):
        return self.name

class UserBadge(models.Model):
    """
    Connects a user to a badge.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="badges")
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'badge')

class Certificate(models.Model):
    """
    Official completion document for a Course.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="certificates")
    
    # We link to the Course app (String reference avoids circular imports)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    
    issued_at = models.DateTimeField(auto_now_add=True)
    
    # We can store the generated PDF URL if we upload to S3, 
    # or just regenerate it on the fly to save space.
    pdf_file = models.FileField(upload_to="certificates/", blank=True, null=True)

    def __str__(self):
        return f"Certificate: {self.user} - {self.course}"