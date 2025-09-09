# -----------------------------
# Base image
# -----------------------------
    FROM python:3.11-slim AS base

    # -----------------------------
    # Environment variables
    # -----------------------------
    ENV PYTHONDONTWRITEBYTECODE=1 \
        PYTHONUNBUFFERED=1 \
        PORT=8000 \
        DJANGO_SETTINGS_MODULE=mcp_integration.settings
    
    # -----------------------------
    # Install system dependencies
    # -----------------------------
    RUN apt-get update \
        && apt-get install -y --no-install-recommends \
            postgresql-client \
            build-essential \
            libpq-dev \
        && rm -rf /var/lib/apt/lists/*
    
    # -----------------------------
    # Set working directory
    # -----------------------------
    WORKDIR /app
    
    # -----------------------------
    # Install Python dependencies
    # -----------------------------
    COPY requirements.txt .
    RUN pip install --no-cache-dir --upgrade pip \
        && pip install --no-cache-dir -r requirements.txt
    
    # -----------------------------
    # Copy project files
    # -----------------------------
    COPY . .
    
    # -----------------------------
    # Set working directory to Django project
    # -----------------------------
    WORKDIR /app/mcp_integration
    
    # -----------------------------
    # Create non-root user
    # -----------------------------
    RUN adduser --disabled-password --gecos '' appuser \
        && chown -R appuser:appuser /app
    
    USER appuser
    
    # -----------------------------
    # Collect static files
    # -----------------------------
    RUN python manage.py collectstatic --noinput
    
    # -----------------------------
    # Expose port
    # -----------------------------
    EXPOSE 8000
    
    # -----------------------------
    # Start the application
    # -----------------------------
    COPY start.sh /app/start.sh
    RUN chmod +x /app/start.sh
    
    CMD ["/app/start.sh"]
    