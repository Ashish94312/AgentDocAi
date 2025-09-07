"""
URL configuration for mcp_integration project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def health_check(request):
    """Simple health check endpoint for Railway"""
    try:
        return JsonResponse({
            'status': 'healthy', 
            'message': 'Django app is running',
            'timestamp': __import__('datetime').datetime.now().isoformat(),
            'host': request.get_host(),
            'method': request.method
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

def root_view(request):
    """Simple root view that doesn't depend on templates"""
    return JsonResponse({
        'message': 'AgentDocAI Django Application',
        'status': 'running',
        'endpoints': {
            'health': '/health/',
            'admin': '/admin/',
            'documentation': '/'
        }
    })

# Task 4: Add your application's URLconf 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health_check'),
    path('api/', root_view, name='root_view'),
    path('', include('mcp_manager.urls')),
]