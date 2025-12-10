from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """
    Custom User model for NovaLab.
    """
    class Role(models.TextChoices):
        SUPER_ADMIN = "SUPER_ADMIN", "Super Admin"
        SCHOOL_ADMIN = "SCHOOL_ADMIN", "School Admin"
        TEACHER = "TEACHER", "Teacher"
        STUDENT = "STUDENT", "Student"

    # Base Fields
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.STUDENT)
    email = models.EmailField(_("email address"), unique=True)
    
    # We will uncomment this after we build the Schools app!
    school = models.ForeignKey(
        'schools.School', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='users'
    )

    # Profile Fields
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    bio = models.TextField(blank=True)
    
    # Google Auth often provides 'email_verified'
    is_email_verified = models.BooleanField(default=False)

    # Use email as the login identifier instead of username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.email} ({self.role})"