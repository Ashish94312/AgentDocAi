#!/usr/bin/env bash
set -o errexit

# Change to the mcp_integration directory
cd "$(dirname "$0")"

# Check if virtual environment exists, create if not
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Install gunicorn for production
echo "Installing gunicorn..."
pip install gunicorn

# Check Django configuration
echo "Checking Django configuration..."
python manage.py check

echo "Build completed successfully!"
echo "Production server can be started with: gunicorn mcp_integration.wsgi:application"
