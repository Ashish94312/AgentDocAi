#!/usr/bin/env bash
set -o errexit

echo "Building RepoDoc-AI for Railway deployment..."

# Build the GitHub MCP server
echo "Building GitHub MCP server..."
cd github-mcp-server
go mod download
go build -o github-mcp-server cmd/github-mcp-server/main.go
cd ..

# Set up Python environment
echo "Setting up Python environment..."
cd mcp_integration

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install gunicorn
echo "Installing gunicorn..."
pip install gunicorn

# Run Django setup
echo "Running Django setup..."
python manage.py collectstatic --noinput

echo "Build completed successfully!"
echo "MCP server is available at: $(pwd)/../github-mcp-server/github-mcp-server"
