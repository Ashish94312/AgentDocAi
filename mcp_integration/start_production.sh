#!/usr/bin/env bash
set -o errexit

# Change to the mcp_integration directory
cd "$(dirname "$0")"

echo "Current directory: $(pwd)"
echo "PORT environment variable: $PORT"

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start gunicorn server
echo "Starting gunicorn server on port ${PORT:-10000}..."
exec gunicorn mcp_integration.wsgi:application \
    --bind 0.0.0.0:${PORT:-10000} \
    --workers 1 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --preload
