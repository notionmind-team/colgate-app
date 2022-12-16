from django.urls import path
from . import views
from . import superadmin_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView

urlpatterns = [
    #user
    path('login', views.login,name='api_user_login'),
    path('logout', views.logout,name='api_user_logout'),
    path('source-create',superadmin_views.source_create,name='source_create'),
    path('source-listing',superadmin_views.source_listing,name='source_listing'),
    path('source-update',superadmin_views.source_update,name='source_update'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)