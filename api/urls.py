from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView

urlpatterns = [
    #user
    path('login', views.login,name='api_user_login'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)