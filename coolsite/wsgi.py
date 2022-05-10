import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coolsite.settings')

import django
django.setup()

application = get_wsgi_application()