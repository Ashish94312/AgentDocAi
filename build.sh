#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r mcp_integration/requirements.txt

# Change to Django app directory
cd mcp_integration

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput
