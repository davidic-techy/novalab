import os
import sys
import django
from pathlib import Path

# Setup Path to find 'config'
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def run():
    email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@novalab.io")
    password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "admin123")

    if not User.objects.filter(email=email).exists():
        print(f"Creating Superuser: {email}")
        User.objects.create_superuser(
            username=email,  # <--- FIX: Use email as the username
            email=email,
            password=password,
            first_name="Super",
            last_name="Admin"
        )
    else:
        print("Superuser already exists.")

if __name__ == "__main__":
    run()