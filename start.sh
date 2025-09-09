#!/bin/bash
set -e

echo "Starting Django application..."
echo "Current directory: $(pwd)"
echo "Contents: $(ls -la)"

# Change to Django project directory
cd /app/mcp_integration
echo "Changed to Django project directory: $(pwd)"

# Check Django configuration
echo "Checking Django configuration..."
python manage.py check

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Health check removed - no longer needed

# Start Gunicorn
NUM_WORKERS=${GUNICORN_WORKERS:-3}
echo "Starting Gunicorn on port ${PORT:-8000} with ${NUM_WORKERS} workers..."
exec gunicorn --bind 0.0.0.0:${PORT:-8000} \
             --workers ${NUM_WORKERS} \
             --timeout 120 \
             --access-logfile - \
             --error-logfile - \
             mcp_integration.wsgi:application
