
from django.urls import path
from . import views



urlpatterns = [
    path('', views.documentation_interface, name='documentation_interface'),
    path('generate/', views.generate_documentation, name='generate_documentation'),
    path('generate-async/', views.generate_documentation_async, name='generate_documentation_async'),
    path('api/generate-async/', views.generate_documentation_api_async, name='generate_documentation_api_async'),
]