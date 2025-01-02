import os

import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_service.settings')
django.setup()
