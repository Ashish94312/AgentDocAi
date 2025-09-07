#!/bin/bash
set -e

echo "Starting Django application..."

# Run migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files (if not already done during build)
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start gunicorn
echo "Starting Gunicorn server on port ${PORT:-8000}..."
exec gunicorn --bind 0.0.0.0:${PORT:-8000} --workers 3 --timeout 120 mcp_integration.wsgi:application
