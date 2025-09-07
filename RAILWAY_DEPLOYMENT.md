# Railway Deployment Guide

## Overview
This guide will help you deploy your Django application to Railway.

## Prerequisites
- Railway account (sign up at [railway.app](https://railway.app))
- GitHub repository with your code
- Environment variables ready

## Deployment Steps

### 1. Connect to Railway
1. Go to [railway.app](https://railway.app) and sign in
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository

### 2. Configure Environment Variables
In your Railway project dashboard, go to Variables and add:

```bash
# Required
SECRET_KEY=your-super-secret-django-key-here
DEBUG=False
ALLOWED_HOSTS=your-app-name.railway.app,localhost,127.0.0.1

# Database (Railway will provide these automatically)
PGDATABASE=railway
PGUSER=postgres
PGPASSWORD=your-password
PGHOST=your-host
PGPORT=5432

# API Keys
OPENAI_API_KEY=your-openai-api-key
GITHUB_PERSONAL_ACCESS_TOKEN=your-github-token
```

### 3. Add PostgreSQL Database
1. In your Railway project, click "New"
2. Select "Database" → "PostgreSQL"
3. Railway will automatically set the database environment variables

### 4. Deploy
1. Railway will automatically detect your Dockerfile
2. The deployment will start automatically
3. Monitor the build logs in the Railway dashboard

### 5. Run Migrations
After deployment, you may need to run migrations:

1. Go to your service in Railway dashboard
2. Click on the service
3. Go to "Deployments" tab
4. Click on the latest deployment
5. Go to "Logs" tab
6. You can run commands using Railway CLI or add a release command

## Railway CLI Commands

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Link to your project
railway link

# Run migrations
railway run python manage.py migrate

# Create superuser
railway run python manage.py createsuperuser

# Collect static files
railway run python manage.py collectstatic --noinput
```

## Environment Variables Reference

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `SECRET_KEY` | Django secret key | Yes | - |
| `DEBUG` | Debug mode | Yes | `False` |
| `ALLOWED_HOSTS` | Allowed hosts (comma-separated) | Yes | `localhost,127.0.0.1` |
| `PGDATABASE` | PostgreSQL database name | Auto | `railway` |
| `PGUSER` | PostgreSQL username | Auto | `postgres` |
| `PGPASSWORD` | PostgreSQL password | Auto | - |
| `PGHOST` | PostgreSQL host | Auto | - |
| `PGPORT` | PostgreSQL port | Auto | `5432` |
| `OPENAI_API_KEY` | OpenAI API key | Optional | - |
| `GITHUB_PERSONAL_ACCESS_TOKEN` | GitHub token | Optional | - |

## Troubleshooting

### Common Issues

1. **Build Fails**
   - Check Dockerfile syntax
   - Ensure all dependencies are in requirements.txt
   - Check build logs in Railway dashboard

2. **Database Connection Issues**
   - Verify PostgreSQL service is running
   - Check environment variables are set correctly
   - Ensure migrations are run

3. **Static Files Not Loading**
   - Verify WhiteNoise is configured
   - Check STATIC_ROOT setting
   - Ensure collectstatic runs during build

4. **Application Not Starting**
   - Check CMD in Dockerfile
   - Verify PORT environment variable
   - Check application logs

### Useful Commands

```bash
# Check application status
railway status

# View logs
railway logs

# Connect to database
railway connect postgres

# Run shell commands
railway run python manage.py shell
```

## Production Checklist

- [ ] Set `DEBUG=False`
- [ ] Set strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up PostgreSQL database
- [ ] Configure environment variables
- [ ] Run migrations
- [ ] Test application functionality
- [ ] Set up monitoring (optional)
- [ ] Configure custom domain (optional)

## Support

- Railway Documentation: [docs.railway.app](https://docs.railway.app)
- Railway Discord: [discord.gg/railway](https://discord.gg/railway)
- Railway Support: [railway.app/support](https://railway.app/support)
