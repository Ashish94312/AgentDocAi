"""
WSGI config for mcp_integration project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# Use the main settings module for all environments
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mcp_integration.settings')

application = get_wsgi_application()