from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from uploader.views import register


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('uploader.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)