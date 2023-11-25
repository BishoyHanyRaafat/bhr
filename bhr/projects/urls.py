from django.contrib import admin
from django.urls import path
from .views import projects, return_project, certificates, return_certificates
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('projects/',projects),
    path('projects/<int:project_id>',return_project),
    path('certificates/',certificates),
    path('certificates/<int:certificate_id>', return_certificates),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)