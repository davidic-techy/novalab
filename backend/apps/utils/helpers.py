import uuid
import random
import string
from django.utils.text import slugify

def generate_unique_slug(model_class, field_name, title):
    """
    Generates a unique slug for a model.
    e.g. "My Course" -> "my-course", then "my-course-1", "my-course-2" if duplicates exist.
    """
    origin_slug = slugify(title)
    unique_slug = origin_slug
    numb = 1
    
    # Loop until we find a slug that doesn't exist in the DB
    while model_class.objects.filter(**{field_name: unique_slug}).exists():
        unique_slug = f'{origin_slug}-{numb}'
        numb += 1
        
    return unique_slug

def generate_random_code(length=6):
    """
    Generates a random alphanumeric code (e.g., for invite codes).
    """
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def get_client_ip(request):
    """
    Retrieves the IP address from the request (handles proxy headers).
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    return (
        x_forwarded_for.split(',')[0]
        if x_forwarded_for
        else request.META.get('REMOTE_ADDR')
    )