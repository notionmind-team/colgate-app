from django.urls import path
from . import views
from . import superadmin_views
from . import user_views
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
    path('source-delete',superadmin_views.source_delete,name='source_delete'),
    path('source-server-create',superadmin_views.source_server_create,name='source_server_create'),
    path('source-server-listing',superadmin_views.source_server_listing,name='source_server_listing'),
    path('source-server-details',superadmin_views.source_server_details,name='source_server_details'),
    path('source-server-update',superadmin_views.source_server_update,name='source_server_update'),
    path('source-server-delete',superadmin_views.source_server_delete,name='source_server_delete'),
    path('user-create',superadmin_views.user_create,name='user_create'),
    path('user-listing',superadmin_views.user_listing,name='user_listing'),
    path('user-update',superadmin_views.user_update,name='user_update'),
    path('dashboard-listing',superadmin_views.dashboard_listing,name='dashboard_listing'),


    path('user-dashboard-create',user_views.user_dashboard_create,name='dashboard_listing'),
    path('user-dashboard-listing',user_views.user_dashboard_listing,name='user_dashboard_listing'),
    path('user-dashboard-details',user_views.user_dashboard_details,name='user_dashboard_details'),
    path('user-dashboard-update',user_views.user_dashboard_update,name='user_dashboard_update'),
    path('user-dashboard-delete',user_views.user_dashboard_delete,name='user_dashboard_delete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)