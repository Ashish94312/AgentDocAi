#!/bin/bash
set -e

echo "Starting Django application..."
echo "Current directory: $(pwd)"
echo "Contents: $(ls -la)"

# Check Django configuration
echo "Checking Django configuration..."
python manage.py check

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Optional health check
if [ "${CHECK_HEALTH:-true}" = "true" ]; then
    echo "Testing health endpoint..."
    python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mcp_integration.settings')
django.setup()
from django.test import Client
client = Client()
response = client.get('/health/')
print(f'Health endpoint status: {response.status_code}')
"
fi

# Start Gunicorn
NUM_WORKERS=${GUNICORN_WORKERS:-3}
echo "Starting Gunicorn on port ${PORT:-8000} with ${NUM_WORKERS} workers..."
exec gunicorn --bind 0.0.0.0:${PORT:-8000} \
             --workers ${NUM_WORKERS} \
             --timeout 120 \
             --access-logfile - \
             --error-logfile - \
             mcp_integration.wsgi:application
