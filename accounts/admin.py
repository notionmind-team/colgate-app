from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import   UserAdmin as DjangoAdminUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from .models import *
from django.contrib.admin import SimpleListFilter
from django.urls import path, include, re_path
from datetime import date
from django.http.response import  HttpResponseRedirect, HttpResponse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.conf import settings
from django.apps import apps

#admin users
class UserAdmin(BaseUserAdmin):
    
    list_display = ('date_joined','role','first_name','last_name','email','mobile','is_staff')
    list_filter = ('role', 'groups', 'date_joined','is_staff')
    fieldsets = (
        (None, {'fields': ('role', 'first_name','last_name', 'mobile','designation','company','email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions','isProfileComplete','isTermAccepted','isEulaAccepted','isDeleted')}),
        ('Other Information', {'fields': ('source','ipaddress', 'browserinfo',)}),

    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'role','first_name','last_name','email','mobile','password1','password2',
                )
            }
        ),
    )
    search_fields       = ('first_name', 'last_name', 'email', 'mobile')
    ordering            = ('-date_joined',)

#role admin
class RoleAdmin(admin.ModelAdmin):
    
    list_display = ('name','publish')



models = apps.get_models()
admin.site.register(User,UserAdmin)
admin.site.register(Role,RoleAdmin)

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass

