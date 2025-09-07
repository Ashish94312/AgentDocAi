FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Copy and setup startup script (before user switch)
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Set Django settings
ENV DJANGO_SETTINGS_MODULE=mcp_integration.settings

# Collect static files
WORKDIR /app/mcp_integration
RUN python manage.py collectstatic --noinput

# Create a non-root user
RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser:appuser /app
USER appuser

# Expose port (Railway will set the actual port)
EXPOSE 8000

# Use startup script
CMD ["/app/start.sh"]
