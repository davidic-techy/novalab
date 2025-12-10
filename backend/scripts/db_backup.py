import os
import sys
import django
from django.core.management import call_command
from django.utils import timezone
from pathlib import Path

# --- FIX: Add the project root to the python path ---
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
# ----------------------------------------------------

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")
django.setup()

# Import settings after setup
from django.conf import settings

def run():
    timestamp = timezone.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"backup_{timestamp}.json"
    
    # Ensure backups folder exists at the project root
    backup_dir = os.path.join(settings.BASE_DIR, 'backups')
    os.makedirs(backup_dir, exist_ok=True)
    
    file_path = os.path.join(backup_dir, filename)

    print(f"Backing up database to {file_path}...")
    
    with open(file_path, 'w') as f:
        # Exclude content types and sessions to keep backup clean
        call_command('dumpdata', exclude=['contenttypes', 'sessions'], stdout=f)
    
    print("Backup Complete.")

if __name__ == "__main__":
    run()