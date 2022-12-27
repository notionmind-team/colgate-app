
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

@api_view(["POST"])
def user_create(request):
    if request.user.is_anonymous:
        errormsg = "Bad Request"
        return Response(data={"status":"Error","message":errormsg}, status=HTTP_400_BAD_REQUEST)
    
    if request.user.role.role_type == ROLE_SUPER_ADMIN:
        try:
            refresh_token(request.user)
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            email = request.POST.get("email")
            password = request.POST.get("password")
            role_type = request.POST.get("role_type")
            
            if first_name.strip() == "":
                errormsg = "The first name can not be empty."
                return Response({"status":"Error","message":errormsg},status=HTTP_200_OK)
            
            if last_name.strip() == "":
                errormsg = "The last name can not be empty."
                return Response({"status":"Error","message":errormsg},status=HTTP_200_OK)

            if email.strip() == "":
                errormsg = "The email can not be empty."
                return Response({"status":"Error","message":errormsg},status=HTTP_200_OK)

            if password.strip() == "":
                errormsg = "The email can not be empty."
                return Response({"status":"Error","message":errormsg},status=HTTP_200_OK)

            email = email.lower()

            userfound = User.objects.filter(email=email).first()
            if userfound:
                errormsg = "Email is already used."
                return Response({"status":"Error","message":errormsg},status=HTTP_200_OK)
                
            role = ""
            role_type = role_type.upper()

            if role_type == "ADMIN" or role_type == ROLE_SUPER_ADMIN:
                role = Role.objects.filter(role_type=ROLE_SUPER_ADMIN).first()
            elif role_type == "USER":
                role = Role.objects.filter(role_type=ROLE_USER).first()
            else:
                errormsg = "role does not match."
                return Response({"status":"Error","message":errormsg},status=HTTP_200_OK)

            user = User.objects.create(
                role = role,
                first_name = first_name,
                last_name = last_name,
                email = email,
                mobile = '', 
                designation = '',
                company = '',
                isDeleted = False,
                isTermAccepted = False,
                isEulaAccepted=False,
                isProfileComplete = True,
                source = 'Web'
            )

            user.set_password(password)
            user.save()
        
            return Response(data={"status":"Success","message":"user created sucessfully."}, status=HTTP_200_OK)
        except Exception as e:
            SaveLog(e)
            return Response(data={"status":"Error","message":SERVER_ERROR}, status=HTTP_200_OK)
    else:
        errormsg = "Bad Request"
        return Response(data={"status":"Error","message":errormsg}, status=HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def user_listing(request):
    role = Role.objects.filter(role_type=ROLE_USER).first()
    user_list = User.objects.filter(role=role).order_by("first_name")

    res_list = []
    for user in user_list:
        data = {}
        data["id"] = ValueCheck(user.id)
        data["name"] = ValueCheck(user.first_name) + " " + ValueCheck(user.last_name)
        data["email"] = ValueCheck(user.email)
        data["role"] = ValueCheck(user.role)
        if user.isDeleted:
            data["is_active"] = False
        else:
            data["is_active"] = True

        res_list.append(data)

    if len(res_list) == 0:
        return Response(data={"status":"Error","message":"User record not found."}, status=HTTP_200_OK)

    return Response(data={"status":"Success","message":"All user list get successfully.","data":res_list}, status=HTTP_200_OK)

@api_view(["POST"])
def user_update(request):
    user_id = request.POST.get("user_id")
    active = checkTrueOrFalse(request.POST.get("is_active"))
    
    if user_id == "":
        errormsg = "User id can not be empty."
        return Response({"status":"Error","message":errormsg},status=HTTP_200_OK)

    role = Role.objects.filter(role_type=ROLE_USER).first()
    user = User.objects.filter(id=user_id,role=role).first()
    if user is None:
        return Response({"status":"Error","message":"Unable to find user data."},status=HTTP_200_OK)
    
    if active:
        user.isDeleted = False
    else:
        user.isDeleted = True
    user.save()

    return Response(data={"status":"Success","message":"user updated successfully."}, status=HTTP_200_OK)


@api_view(["POST"])
def dashboard_listing(request):
    source_name = request.POST.get("source_name")
    if source_name == "":
        errormsg = "Source name can not be empty."
        return Response({"status":"Error","message":errormsg},status=HTTP_200_OK)
    
    source_uppercase = source_name.upper()
    response_data = []
    
    if source_uppercase == "DOMO":
        dashboard_list = GetDomoDashboardList()
        for dashboard_res in dashboard_list:

            dashboard_obj = DashboardDetails.objects.filter(dashboard_id=str(dashboard_res["id"])).first()
            if dashboard_obj:
                dashboard_obj.name = dashboard_res["name"]
                dashboard_obj.link = ""
                dashboard_obj.dashboard_id = str(dashboard_res["id"])
                dashboard_obj.source_type = "DOMO"
                dashboard_obj.createdBy = request.user
                dashboard_obj.save()
            else:
                dashboard_obj = DashboardDetails.objects.create(
                    name=dashboard_res["name"],
                    link="",
                    source_type = "DOMO",
                    dashboard_id=str(dashboard_res["id"]),
                    createdBy = request.user,
                )

            data = {}
            data["name"] = dashboard_obj.name
            data["link"] = dashboard_obj.link
            data["dashboard_id"] = dashboard_obj.dashboard_id
            data["source_type"] = dashboard_obj.source_type
            response_data.append(data)

    return Response(data={"status":"Success","message":"dashboard list.", "data":response_data}, status=HTTP_200_OK)
