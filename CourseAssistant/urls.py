from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from base.views import install_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('stats/', include('stats.urls')),
    path('chat/', include('chat.urls')),
    path('install/', install_page, name='install'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
