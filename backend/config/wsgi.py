import os
from django.core.wsgi import get_wsgi_application

# Point to our settings file
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')

application = get_wsgi_application()