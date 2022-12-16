
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



db_logger = logging.getLogger('accounts')

#user login
@api_view(["POST",])
@permission_classes((hasKey,))
def login(request):
    try:
        email       = request.data.get("email")
        password    = request.data.get("password")

        if email == "" or password == "":
            return Response(data={"status":"Error","message":"Please enter your email address and password."}, status=HTTP_200_OK)
        
        email = email.lower()

        user = User.objects.filter(email=email).first()
        if user is None:
            return Response(data={"status":"Error","message":"This email address does not exist."}, status=HTTP_200_OK)

        email = user.email
        user = authenticate(email=email, password=password,)
        
        #assert False
        if not user:
            return Response(data={"status":"Error","message":"Invalid email or password."}, status=HTTP_200_OK)
        
        if user.isDeleted:
            return Response(data={"status":"Error","message":"This account is not active. Please contact the admin at help@suretytech.ca"}, status=HTTP_200_OK)

        token, created = Token.objects.get_or_create(user=user)
        if not created:
            utc_now = datetime.datetime.utcnow()
            utc_now = utc_now.replace(tzinfo=pytz.utc)
            token.created = utc_now
            token.save()
        auth_login(request._request, user)

        role = 'superadmin'
        if user.role:
            role= user.role.role_type

        company = ""
        if user.company:
            company = user.company

        designation = ""
        if user.designation:
            designation = user.designation

        mobile = ""
        if user.mobile:
            mobile = user.mobile

        email = ""
        if user.email:
            email = user.email
        
        first_name = ""
        if user.first_name:
            first_name = user.first_name

        last_name = ""
        if user.last_name:
            last_name = user.last_name

        return Response(data={"status":"Success","message":"Logged In","data":{"token":token.key,"email":email,"mobile":mobile,"company":company,"designation":designation,"role":role,"first_name":first_name,"last_name":last_name}}, status=HTTP_200_OK)
    except Exception as e:
        SaveLog(e)
        return Response(data={"status":"Error","message":SERVER_ERROR}, status=HTTP_200_OK)


#user logout
@api_view(["GET",])
def logout(request):
    
    if request.user:
        token = Token.objects.get(user=request.user)
        token.delete()
        auth_logout(request._request)

    return Response(data={"status":"Success","message":"Logged Out"},status=HTTP_200_OK)