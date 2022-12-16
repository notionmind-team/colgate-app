from rest_framework.authentication import TokenAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth import logout as auth_logout
import datetime
import pytz

def refresh_token(user):
    token = Token.objects.get(user=user)
    utc_now = datetime.datetime.utcnow()
    utc_now = utc_now.replace(tzinfo=pytz.utc)
    token.created = utc_now
    token.save()

class ExpireTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        try:
            token= Token.objects.get(key=key)
        except:
            raise AuthenticationFailed('Invalid Token')

        if not token.user.is_active:
            raise AuthenticationFailed('User inactive of deleted')

        try:
            delta = settings.TOKEN_EXPIRE_PERIOD
        except:
            raise ValueError("Not a Valid Token Expire Time Delta: must be a positive integer")

        utc_now = datetime.datetime.utcnow()
        utc_now = utc_now.replace(tzinfo=pytz.utc)
        
        if utc_now - token.created > delta:
            token.delete()
            raise AuthenticationFailed("Session Timeout!")
        return token.user, token
