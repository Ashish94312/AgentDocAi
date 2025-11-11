from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def root_view(request):
    return JsonResponse({
        'message': 'AgentDocAI Django Application',
        'status': 'running',
        'endpoints': {
            'admin': '/admin/',
            'documentation': '/'
        }
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', root_view, name='root_view'),
    path('', include('mcp_manager.urls')),
]