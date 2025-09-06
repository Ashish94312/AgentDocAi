# Multi-stage build for RepoDoc-AI with MCP server
FROM golang:1.21-alpine AS mcp-builder

# Install build dependencies
RUN apk add --no-cache git

# Build the GitHub MCP server
WORKDIR /app/github-mcp-server
COPY github-mcp-server/ .
RUN go mod download
RUN go build -o github-mcp-server cmd/github-mcp-server/main.go

# Python application stage
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
        curl \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy and install Python dependencies
COPY mcp_integration/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the built MCP server from the builder stage
COPY --from=mcp-builder /app/github-mcp-server/github-mcp-server /app/github-mcp-server/

# Copy the Django application
COPY mcp_integration/ /app/

# Create staticfiles directory
RUN mkdir -p /app/staticfiles

# Collect static files
RUN python manage.py collectstatic --noinput

# Create a non-root user
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "mcp_integration.wsgi:application"]
