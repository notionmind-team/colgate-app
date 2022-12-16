
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
import qrcode


@api_view(["POST"])
def source_create(request):
    if request.user.is_anonymous:
        errormsg = "Bad Request"
        return Response(data={"status":"Error","message":errormsg}, status=HTTP_400_BAD_REQUEST)
    
    if request.user.role.role_type == ROLE_SUPER_ADMIN:
        try:
            refresh_token(request.user)
            user_filter = User.objects.filter(email=request.user.email,isDeleted=True).first()
            if user_filter:
                return Response(data={"status":"Error","message":"This account is not active."}, status=HTTP_200_OK)
          
            source_name = request.POST.get('source_name')
            source_description = request.POST.get("source_description")
            source_image = request.POST.get("source_image")
  
            if source_name == "":
                return Response({"status":"Error","message":"Source name can not empty."},status=HTTP_200_OK)

            if source_description == "":
                return Response({"status":"Error","message":"Source description can not empty."},status=HTTP_200_OK)

            if source_image == "":
                return Response({"status":"Error","message":"Source image can not empty."},status=HTTP_200_OK)

            source_details = SourceDetails.objects.create(
                name=source_name,
                discription=source_description,
                image_url=source_image,
            )
          
            return Response(data={"status":"Success","message":"Source created sucessfully.","data":SourceDetailsSerializer(source_details).data}, status=HTTP_200_OK)

        except Exception as e:
            SaveLog(e)
            return Response(data={"status":"Error","message":SERVER_ERROR}, status=HTTP_200_OK)
    else:
        errormsg = "Bad Request"
        return Response(data={"status":"Error","message":errormsg}, status=HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def source_listing(request):
    if request.user.is_anonymous:
        errormsg = "Bad Request"
        return Response(data={"status":"Error","message":errormsg}, status=HTTP_400_BAD_REQUEST)
    
    if request.user.role.role_type == ROLE_SUPER_ADMIN:
        try:
            refresh_token(request.user)
            user_filter = User.objects.filter(email=request.user.email,isDeleted=True).first()
            if user_filter:
                return Response(data={"status":"Error","message":"This account is not active."}, status=HTTP_200_OK)
          
            source_details = SourceDetails.objects.filter(is_active=True).order_by("-id")
            return Response(data={"status":"Success","message":"Source created sucessfully.","data":SourceDetailsSerializer(source_details,many=True).data}, status=HTTP_200_OK)

        except Exception as e:
            SaveLog(e)
            return Response(data={"status":"Error","message":SERVER_ERROR}, status=HTTP_200_OK)
    else:
        errormsg = "Bad Request"
        return Response(data={"status":"Error","message":errormsg}, status=HTTP_400_BAD_REQUEST)



@api_view(["POST"])
def source_update(request):
    if request.user.is_anonymous:
        errormsg = "Bad Request"
        return Response(data={"status":"Error","message":errormsg}, status=HTTP_400_BAD_REQUEST)
    
    if request.user.role.role_type == ROLE_SUPER_ADMIN:
        try:
            refresh_token(request.user)
            user_filter = User.objects.filter(email=request.user.email,isDeleted=True).first()
            if user_filter:
                return Response(data={"status":"Error","message":"This account is not active."}, status=HTTP_200_OK)
          
            source_id = request.POST.get('source_id')    
            source_name = request.POST.get('source_name')
            source_description = request.POST.get("source_description")
            source_image = request.POST.get("source_image")

            if source_id == "":
                return Response({"status":"Error","message":"Source id can not empty."},status=HTTP_200_OK)
  
            if source_name == "":
                return Response({"status":"Error","message":"Source name can not empty."},status=HTTP_200_OK)

            if source_description == "":
                return Response({"status":"Error","message":"Source description can not empty."},status=HTTP_200_OK)

            if source_image == "":
                return Response({"status":"Error","message":"Source image can not empty."},status=HTTP_200_OK)

            source_detail = SourceDetails.objects.filter(id=source_id,is_active=True).first()
            if source_detail is None:
                return Response({"status":"Error","message":"Source not found."},status=HTTP_200_OK)

            source_detail.name=source_name
            source_detail.discription=source_description
            source_detail.image_url=source_image
            source_detail.save()
            
          
            return Response(data={"status":"Success","message":"Source updated sucessfully.","data":SourceDetailsSerializer(source_detail).data}, status=HTTP_200_OK)

        except Exception as e:
            SaveLog(e)
            return Response(data={"status":"Error","message":SERVER_ERROR}, status=HTTP_200_OK)
    else:
        errormsg = "Bad Request"
        return Response(data={"status":"Error","message":errormsg}, status=HTTP_400_BAD_REQUEST)


##### source server

@api_view(["POST"])
def source_server_create(request):
    if request.user.is_anonymous:
        errormsg = "Bad Request"
        return Response(data={"status":"Error","message":errormsg}, status=HTTP_400_BAD_REQUEST)
    
    if request.user.role.role_type == ROLE_SUPER_ADMIN:
        try:
            refresh_token(request.user)
            user_filter = User.objects.filter(email=request.user.email,isDeleted=True).first()
            if user_filter:
                return Response(data={"status":"Error","message":"This account is not active."}, status=HTTP_200_OK)
          
            source_id = request.POST.get('source_id')
            server_name = request.POST.get('server_name')
            server_host = request.POST.get('server_host')
            server_port = request.POST.get("server_port")
            username = request.POST.get("username")
            password = request.POST.get("password")
  
            if source_id == "":
                return Response({"status":"Error","message":"source id can not empty."},status=HTTP_200_OK)

            if server_host == "":
                return Response({"status":"Error","message":"source host can not empty."},status=HTTP_200_OK)

            if server_name == "":
                return Response({"status":"Error","message":"server name can not empty."},status=HTTP_200_OK)

            if server_port == "":
                return Response({"status":"Error","message":"server port can not empty."},status=HTTP_200_OK)

            if username == "":
                return Response({"status":"Error","message":"username can not empty."},status=HTTP_200_OK)

            if password == "":
                return Response({"status":"Error","message":"password can not empty."},status=HTTP_200_OK)

            source_detail = SourceDetails.objects.filter(id=source_id,is_active=True).first()
            if source_detail is None:
                return Response({"status":"Error","message":"Source not found."},status=HTTP_200_OK)

            source_server = SourceServer.objects.create(
                source=source_detail,
                serverhost=server_host,
                servername=server_name,
                serverport=server_port,
                username=username,
                password=password,
            )
          
            return Response(data={"status":"Success","message":"Server created sucessfully.","data":SourceServerDetailsSerializer(source_server).data}, status=HTTP_200_OK)

        except Exception as e:
            SaveLog(e)
            return Response(data={"status":"Error","message":SERVER_ERROR}, status=HTTP_200_OK)
    else:
        errormsg = "Bad Request"
        return Response(data={"status":"Error","message":errormsg}, status=HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def source_server_listing(request):
    if request.user.is_anonymous:
        errormsg = "Bad Request"
        return Response(data={"status":"Error","message":errormsg}, status=HTTP_400_BAD_REQUEST)
    
    if request.user.role.role_type == ROLE_SUPER_ADMIN:
        try:
            refresh_token(request.user)
            user_filter = User.objects.filter(email=request.user.email,isDeleted=True).first()
            if user_filter:
                return Response(data={"status":"Error","message":"This account is not active."}, status=HTTP_200_OK)
            
            source_id = request.POST.get('source_id')    
            if source_id == "":
                return Response({"status":"Error","message":"Source id can not empty."},status=HTTP_200_OK)
            
            source_detail = SourceDetails.objects.filter(id=source_id,is_active=True).first()
            if source_detail is None:
                return Response({"status":"Error","message":"Source not found."},status=HTTP_200_OK)
                
            server_details = SourceServer.objects.filter(is_active=True,source=source_detail).order_by("-id")
            return Response(data={"status":"Success","message":"source listing sucessfully.","data":SourceServerDetailsSerializer(server_details,many=True).data}, status=HTTP_200_OK)

        except Exception as e:
            SaveLog(e)
            return Response(data={"status":"Error","message":SERVER_ERROR}, status=HTTP_200_OK)
    else:
        errormsg = "Bad Request"
        return Response(data={"status":"Error","message":errormsg}, status=HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def source_server_details(request):
    if request.user.is_anonymous:
        errormsg = "Bad Request"
        return Response(data={"status":"Error","message":errormsg}, status=HTTP_400_BAD_REQUEST)
    
    if request.user.role.role_type == ROLE_SUPER_ADMIN:
        try:
            refresh_token(request.user)
            user_filter = User.objects.filter(email=request.user.email,isDeleted=True).first()
            if user_filter:
                return Response(data={"status":"Error","message":"This account is not active."}, status=HTTP_200_OK)
            
            server_id = request.POST.get('server_id')    
            if server_id == "":
                return Response({"status":"Error","message":"server id can not empty."},status=HTTP_200_OK)
            
            server_detail = SourceServer.objects.filter(id=server_id,is_active=True).first()
            if server_detail is None:
                return Response({"status":"Error","message":"server detail not found."},status=HTTP_200_OK)
                
            return Response(data={"status":"Success","message":"server details get sucessfully.","data":SourceServerDetailsSerializer(server_detail).data}, status=HTTP_200_OK)

        except Exception as e:
            SaveLog(e)
            return Response(data={"status":"Error","message":SERVER_ERROR}, status=HTTP_200_OK)
    else:
        errormsg = "Bad Request"
        return Response(data={"status":"Error","message":errormsg}, status=HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def source_server_update(request):
    if request.user.is_anonymous:
        errormsg = "Bad Request"
        return Response(data={"status":"Error","message":errormsg}, status=HTTP_400_BAD_REQUEST)
    
    if request.user.role.role_type == ROLE_SUPER_ADMIN:
        try:
            refresh_token(request.user)
            user_filter = User.objects.filter(email=request.user.email,isDeleted=True).first()
            if user_filter:
                return Response(data={"status":"Error","message":"This account is not active."}, status=HTTP_200_OK)
          
            source_id = request.POST.get('source_id')
            server_id = request.POST.get('server_id')
            server_name = request.POST.get('server_name')
            server_host = request.POST.get('server_host')
            server_port = request.POST.get("server_port")
            username = request.POST.get("username")
            password = request.POST.get("password")
  
            if source_id == "":
                return Response({"status":"Error","message":"source id can not empty."},status=HTTP_200_OK)

            if server_host == "":
                return Response({"status":"Error","message":"source host can not empty."},status=HTTP_200_OK)

            if server_name == "":
                return Response({"status":"Error","message":"server name can not empty."},status=HTTP_200_OK)

            if server_port == "":
                return Response({"status":"Error","message":"server port can not empty."},status=HTTP_200_OK)

            if username == "":
                return Response({"status":"Error","message":"username can not empty."},status=HTTP_200_OK)

            if password == "":
                return Response({"status":"Error","message":"password can not empty."},status=HTTP_200_OK)

            source_detail = SourceDetails.objects.filter(id=source_id,is_active=True).first()
            if source_detail is None:
                return Response({"status":"Error","message":"Source detail not found."},status=HTTP_200_OK)

            server_detail = SourceServer.objects.filter(id=server_id,is_active=True).first()
            if server_detail is None:
                return Response({"status":"Error","message":"server detail not found."},status=HTTP_200_OK)

            server_detail.source=source_detail
            server_detail.serverhost=server_host
            server_detail.servername=server_name
            server_detail.serverport=server_port
            server_detail.username=username
            server_detail.password=password
            server_detail.save()
        
            return Response(data={"status":"Success","message":"Server updated sucessfully.","data":SourceServerDetailsSerializer(server_detail).data}, status=HTTP_200_OK)

        except Exception as e:
            SaveLog(e)
            return Response(data={"status":"Error","message":SERVER_ERROR}, status=HTTP_200_OK)
    else:
        errormsg = "Bad Request"
        return Response(data={"status":"Error","message":errormsg}, status=HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def source_server_delete(request):
    if request.user.is_anonymous:
        errormsg = "Bad Request"
        return Response(data={"status":"Error","message":errormsg}, status=HTTP_400_BAD_REQUEST)
    
    if request.user.role.role_type == ROLE_SUPER_ADMIN:
        try:
            refresh_token(request.user)
            user_filter = User.objects.filter(email=request.user.email,isDeleted=True).first()
            if user_filter:
                return Response(data={"status":"Error","message":"This account is not active."}, status=HTTP_200_OK)
            
            server_id = request.POST.get('server_id')    
            if server_id == "":
                return Response({"status":"Error","message":"server id can not empty."},status=HTTP_200_OK)
            
            server_detail = SourceServer.objects.filter(id=server_id,is_active=True).first()
            if server_detail is None:
                return Response({"status":"Error","message":"server detail not found."},status=HTTP_200_OK)
            
            server_detail.delete()

            return Response(data={"status":"Success","message":"server deleted sucessfully."}, status=HTTP_200_OK)

        except Exception as e:
            SaveLog(e)
            return Response(data={"status":"Error","message":SERVER_ERROR}, status=HTTP_200_OK)
    else:
        errormsg = "Bad Request"
        return Response(data={"status":"Error","message":errormsg}, status=HTTP_400_BAD_REQUEST)