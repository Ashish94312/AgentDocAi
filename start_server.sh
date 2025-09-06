#!/usr/bin/env bash
set -o errexit

# Change to the mcp_integration directory
cd "$(dirname "$0")/mcp_integration"

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Start Django development server
echo "Starting Django development server..."
echo "Server will be available at: http://127.0.0.1:8000/"
echo "Press Ctrl+C to stop the server"
python manage.py runserver
