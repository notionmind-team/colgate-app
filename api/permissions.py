from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied 
from accounts.models import APIAuthKey


class hasKey(BasePermission):
    def has_permission(self, request, view, obj=None):
        #message="No Access Key"
        key = request.META.get("HTTP_APIKEY")
        #
        # assert False
        try:
            keyobj = APIAuthKey.objects.get(key=key)
        except:
            raise PermissionDenied('Invalid API Key')
            
        if (not keyobj.isRevoked):
            return True
        else:
            raise PermissionDenied("API Key Revoked")