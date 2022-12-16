from accounts.models import *
from rest_framework import serializers, permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.conf import settings
from .constants import *
from datetime import datetime, time
import datetime
from django_db_logger.models import StatusLog
from pytz import timezone

class CurrentUser(object):
    def set_context(self, serializer_field):
        self.user_obj = serializer_field.context['request'].user

    def __call__(self):
        return self.user_obj

#user change password serializer
class ChangePasswordSerializer(serializers.Serializer):
    old_pass        = serializers.CharField()
    new_pass        = serializers.CharField()
    confirm_pass    = serializers.CharField()

    def validate(self, data):
        if data['new_pass']!=data['confirm_pass']:
            raise serializers.ValidationError("Confirm password does not match")
        elif data['new_pass']==data['old_pass']:
            raise serializers.ValidationError("New password can not be same as old password")
        return data

    def validate_new_pass(self, new_pass):
        user = self.context['request'].user
        validate_password(new_pass, user=user)
        return new_pass

    def validate_old_pass(self, old_pass):
        user = self.context['request'].user
        if not user.check_password(old_pass):
            raise serializers.ValidationError("Old password does not match")
        return old_pass

#user create serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= get_user_model()
        fields=("role","name", "email", "mobile", "password","company","designation")
    
    def validate_password(self, password):
        validate_password(password)
        return password

    def create(self, validated_data):
        user=super(UserSerializer,self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
 
#update profile serializer
class UpdateProfileSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField(read_only=True)
    role_name = serializers.ReadOnlyField(source='role.role_type', read_only=True)
    isSiteCreated = serializers.SerializerMethodField(read_only=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for key, value in data.items():
            try:
                if value is None:
                    data[key] = ""
            except KeyError:
                pass
        return data
    
    def get_role(self,ins):
        if ins is None:
            return ""
        if ins.role:
            return str(ins.role.id)
        return ""
    
    def get_isSiteCreated(self, user):
        if Site.objects.filter(user=user, isDeleted = False).count() > 0:
            return True
        else:
            return False
    
    class Meta:
        model   =  get_user_model()
        fields = ("role","role_name","mobile","email","first_name","last_name","company","designation","isProfileComplete","isTermAccepted","isEulaAccepted","isSiteCreated")
        read_only_fields = ('id', 'role_name',"email","first_name","last_name","isSiteCreated","isTermAccepted","isEulaAccepted")

#site admin serializer
class AdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ("first_name","last_name","email","role","mobile","company","designation")
