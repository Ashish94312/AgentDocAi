"""
WSGI config for mcp_integration project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# Use Render settings if RENDER environment variable is set
if os.getenv('RENDER'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mcp_integration.settings_render')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mcp_integration.settings')

application = get_wsgi_application()