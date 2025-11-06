"""
URL configuration for Car2Data project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.authentication.urls')),
    path('dashboard/', include('apps.documents.urls')),
    path('vehicles/', include('apps.vehicles.urls')),
    path('forms/', include('apps.forms_generation.urls')),
    # Social auth routes (allauth) - MUST be before general allauth.urls
    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)