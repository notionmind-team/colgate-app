
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import Group,User
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from accounts.models import *
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response, SimpleTemplateResponse
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from rest_framework.authtoken.models import Token
from django.template.loader import get_template
from .permissions import *
from .authentication import *
from .serializer import *
import datetime
import time
import pytz
import logging
import uuid
import json
from .constants import *
from django.conf import settings
from django.db.models.functions import Lower, Upper
import logging
from django_db_logger.models import StatusLog
from django.http import HttpResponse
from .constants import *
from .helper import *
from .domo import *


@api_view(["POST"])
def user_dashboard_create(request):
    if request.user.is_anonymous:
        errormsg = "Bad Request"
        return Response(data={"status":"Error","message":errormsg}, status=HTTP_400_BAD_REQUEST)
    
    if request.user.role.role_type == ROLE_USER:
        try:
            refresh_token(request.user)
            user_filter = User.objects.filter(email=request.user.email,isDeleted=True).first()
            if user_filter:
                return Response(data={"status":"Error","message":"This account is not active."}, status=HTTP_200_OK)
          
            dashboard_name = request.data.get('dashboard_name')
            image_url = request.data.get("image_url")
 
            if dashboard_name == "":
                return Response({"status":"Error","message":"dashboard name can not empty."},status=HTTP_200_OK)

            userdashboard = UserDashboardDetails.objects.create(
                name=dashboard_name,
                image_url=image_url,
                user=request.user,
            )
          
            return Response(data={"status":"Success","message":"dashboard created sucessfully.","data":UserDashboardDetailsSerializer(userdashboard).data}, status=HTTP_200_OK)

        except Exception as e:
            SaveLog(e)
            return Response(data={"status":"Error","message":SERVER_ERROR}, status=HTTP_200_OK)
    else:
        errormsg = "Bad Request"
        return Response(data={"status":"Error","message":errormsg}, status=HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def user_dashboard_listing(request):
    if request.user.is_anonymous:
        errormsg = "Bad Request"
        return Response(data={"status":"Error","message":errormsg}, status=HTTP_400_BAD_REQUEST)
    
    if request.user.role.role_type == ROLE_USER:
        try:
            refresh_token(request.user)
            user_filter = User.objects.filter(email=request.user.email,isDeleted=True).first()
            if user_filter:
                return Response(data={"status":"Error","message":"This account is not active."}, status=HTTP_200_OK)
          
            userdashboards = UserDashboardDetails.objects.filter(is_active=True,user=request.user)
            return Response(data={"status":"Success","message":"dashboard list get sucessfully.","data":UserDashboardDetailsSerializer(userdashboards,many=True).data}, status=HTTP_200_OK)

        except Exception as e:
            SaveLog(e)
            return Response(data={"status":"Error","message":SERVER_ERROR}, status=HTTP_200_OK)
    else:
        errormsg = "Bad Request"
        return Response(data={"status":"Error","message":errormsg}, status=HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def user_dashboard_details(request):
    if request.user.is_anonymous:
        errormsg = "Bad Request"
        return Response(data={"status":"Error","message":errormsg}, status=HTTP_400_BAD_REQUEST)
    
    if request.user.role.role_type == ROLE_USER:
        try:
            refresh_token(request.user)
            user_filter = User.objects.filter(email=request.user.email,isDeleted=True).first()
            if user_filter:
                return Response(data={"status":"Error","message":"This account is not active."}, status=HTTP_200_OK)
          
            dashboard_id = request.data.get('dashboard_id')
            if dashboard_id == "":
                errormsg = "dashboard_id can not be empty."
                return Response(data={"status":"Error","message":errormsg}, status=HTTP_200_OK)

            userdashboard = UserDashboardDetails.objects.filter(id=dashboard_id).first()
            if userdashboard:
                return Response(data={"status":"Success","message":"dashboard detail get sucessfully.","data":UserDashboardDetailsSerializer(userdashboard).data}, status=HTTP_200_OK)
            else:
                errormsg = "Dashboard can not be found."
                return Response(data={"status":"Error","message":errormsg}, status=HTTP_200_OK)
        except Exception as e:
            SaveLog(e)
            return Response(data={"status":"Error","message":SERVER_ERROR}, status=HTTP_200_OK)
    else:
        errormsg = "Bad Request"
        return Response(data={"status":"Error","message":errormsg}, status=HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def user_dashboard_update(request):
    if request.user.is_anonymous:
        errormsg = "Bad Request"
        return Response(data={"status":"Error","message":errormsg}, status=HTTP_400_BAD_REQUEST)
    
    if request.user.role.role_type == ROLE_USER:
        try:
            refresh_token(request.user)
            user_filter = User.objects.filter(email=request.user.email,isDeleted=True).first()
            if user_filter:
                return Response(data={"status":"Error","message":"This account is not active."}, status=HTTP_200_OK)
          
            dashboard_id = request.data.get('dashboard_id')
            dashboard_name = request.data.get('dashboard_name')
            image_url = request.data.get("image_url")

            if dashboard_id == "":
                errormsg = "dashboard_id can not be empty."
                return Response(data={"status":"Error","message":errormsg}, status=HTTP_200_OK)

            if dashboard_name == "":
                return Response({"status":"Error","message":"dashboard name can not empty."},status=HTTP_200_OK)

            userdashboard = UserDashboardDetails.objects.filter(id=dashboard_id,user=request.user).first()
            if userdashboard:
                userdashboard.name = dashboard_name
                userdashboard.image_url = image_url
                userdashboard.save()
                
                return Response(data={"status":"Success","message":"dashboard updated sucessfully.","data":UserDashboardDetailsSerializer(userdashboard).data}, status=HTTP_200_OK)
            else:
                errormsg = "Dashboard can not be found."
                return Response(data={"status":"Error","message":errormsg}, status=HTTP_200_OK)

        except Exception as e:
            SaveLog(e)
            return Response(data={"status":"Error","message":SERVER_ERROR}, status=HTTP_200_OK)
    else:
        errormsg = "Bad Request"
        return Response(data={"status":"Error","message":errormsg}, status=HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def user_dashboard_delete(request):
    if request.user.is_anonymous:
        errormsg = "Bad Request"
        return Response(data={"status":"Error","message":errormsg}, status=HTTP_400_BAD_REQUEST)
    
    if request.user.role.role_type == ROLE_USER:
        try:
            refresh_token(request.user)
            dashboard_id = request.data.get("dashboard_id")
            
            if dashboard_id == "":
                errormsg = "dashboard_id can not be empty."
                return Response(data={"status":"Error","message":errormsg}, status=HTTP_200_OK)

            user_filter = User.objects.filter(email=request.user.email,isDeleted=True).first()
            if user_filter:
                return Response(data={"status":"Error","message":"This account is not active."}, status=HTTP_200_OK)
          
            userdashboard = UserDashboardDetails.objects.filter(id=dashboard_id,user=request.user).first()
            if userdashboard:
                userdashboard.is_active = False
                userdashboard.save()
            else:
                errormsg = "Dashboard can not be delete."
                return Response(data={"status":"Error","message":errormsg}, status=HTTP_200_OK)

            return Response(data={"status":"Success","message":"dashboard deleted sucessfully."}, status=HTTP_200_OK)

        except Exception as e:
            SaveLog(e)
            return Response(data={"status":"Error","message":SERVER_ERROR}, status=HTTP_200_OK)
    else:
        errormsg = "Bad Request"
        return Response(data={"status":"Error","message":errormsg}, status=HTTP_400_BAD_REQUEST)