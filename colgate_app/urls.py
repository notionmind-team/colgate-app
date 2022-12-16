
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import url, include #djangocms extra
from django.conf import settings #djangocms extra (devserver only)
from django.conf.urls.static import static #djangocms extra (devserver only)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('api.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)