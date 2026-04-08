from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... your existing urlpatterns ...
]

# Serve media files in production (Render) – not ideal but works
if settings.DEBUG or not settings.DEBUG:  # serve always
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)