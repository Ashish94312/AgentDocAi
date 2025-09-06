#!/usr/bin/env bash
set -o errexit

# Change to the mcp_integration directory
cd "$(dirname "$0")"

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate