#!/usr/bin/env bash
set -o errexit

echo "Starting RepoDoc-AI on Railway..."

# Change to the mcp_integration directory
cd mcp_integration

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

# Verify MCP server is available
echo "Checking MCP server availability..."
if [ -f "../github-mcp-server/github-mcp-server" ]; then
    echo "✅ MCP server found and ready!"
    ls -la ../github-mcp-server/github-mcp-server
else
    echo "❌ MCP server not found, but continuing with fallback..."
fi

# Start gunicorn server
echo "Starting gunicorn server on port ${PORT:-10000}..."
exec gunicorn mcp_integration.wsgi:application \
    --bind 0.0.0.0:${PORT:-10000} \
    --workers 1 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --preload
