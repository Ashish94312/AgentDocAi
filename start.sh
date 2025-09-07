#!/bin/bash
set -e

echo "Starting Django application..."

# Check if we're in the right directory
echo "Current directory: $(pwd)"
echo "Contents: $(ls -la)"

# Check Django settings
echo "Checking Django configuration..."
python manage.py check --deploy

# Run migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files (if not already done during build)
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Test that the application can start
echo "Testing Django application startup..."
python manage.py check

# Start gunicorn
echo "Starting Gunicorn server on port ${PORT:-8000}..."
echo "Environment variables:"
echo "PORT: ${PORT:-8000}"
echo "DEBUG: ${DEBUG:-False}"
echo "DJANGO_SETTINGS_MODULE: ${DJANGO_SETTINGS_MODULE:-mcp_integration.settings}"

exec gunicorn --bind 0.0.0.0:${PORT:-8000} --workers 3 --timeout 120 --access-logfile - --error-logfile - mcp_integration.wsgi:application
