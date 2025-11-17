from django.urls import path
from . import views

urlpatterns = [
    path('', views.documentation_interface, name='documentation_interface'),
    path('api/generate/', views.generate_documentation_api_async, name='generate_documentation_api'),
]