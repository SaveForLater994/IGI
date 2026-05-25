"""
WSGI config for Apothecary project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Apothecary.settings')
from django.core.management import call_command

# При запуске сервера принудительно применить миграции
try:
    call_command('migrate')
except Exception as e:
    print(f"Migration error: {e}")
application = get_wsgi_application()
