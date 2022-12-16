
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
import qrcode


db_logger = logging.getLogger('accounts')
SERVER_ERROR = "Sorry, please try again after some time."

#user login
@api_view(["POST",])
@permission_classes((hasKey,))
def login(request):
    return Response(data={"status":"success","message":"ok"}, status=HTTP_200_OK)