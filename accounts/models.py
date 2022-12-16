from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.fields import JSONField
from django.core import serializers


#User Manager Overrite
class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError("The email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user 
    
    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True")
        return self._create_user(email, password, **extra_fields)

#User Role
class Role(models.Model):
    token           = models.UUIDField(default= uuid.uuid4, unique=True)
    role_type       = models.CharField(max_length=20,choices=(('superadmin','superadmin'),('user','user')),default='user')
    name            = models.CharField(max_length=255, unique=True)
    desc            = models.CharField(max_length=255,null=True,blank=True)
    publish         = models.BooleanField(default = True)
    createdAt       = models.DateTimeField(auto_now_add=True)
    updatedAt       = models.DateTimeField(auto_now=True)
    
    def __int__(self):
        return self.id
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name        = "Role"
        verbose_name_plural = "Roles"

#User Model Overrite
class User(AbstractUser):
    token               = models.UUIDField(default= uuid.uuid4, unique=True)
    role                = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    first_name          = models.CharField(max_length=255, null=True, blank=True)
    last_name           = models.CharField(max_length=255, null=True, blank=True)
    email               = models.EmailField(_('email address'), unique=True)
    username            = None
    mobile              = models.CharField(max_length=255, null=True, blank=True)
    designation         = models.CharField(max_length=255, null=True, blank=True)
    company             = models.CharField(max_length=255, null=True, blank=True)
    isDeleted           = models.BooleanField(default=False)
    isTermAccepted      = models.BooleanField(default=False)
    isEulaAccepted      = models.BooleanField(default=False)
    isPasswordSet       = models.BooleanField(default=False)
    isProfileComplete   = models.BooleanField(default=False)
    ipaddress           = models.GenericIPAddressField(null=True, blank=True)
    source              = models.CharField(max_length=10, choices=(('IOS','IOS'),('Android','Android'),('Web','Web')),  default='Web')
    browserinfo         = models.TextField(null=True, blank=True)
    updatedAt           = models.DateTimeField(auto_now=True)
    createdBy           = models.ForeignKey('self', on_delete=models.CASCADE,related_name='user_createdBy', null=True, blank=True)
    updatedBy           = models.ForeignKey('self', on_delete=models.CASCADE,related_name='user_updatedBy', null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    object = UserManager()

    def __int__(self):
        return self.id
    
    def __str__(self):
        return self.email
        
    
    def get_admin_url(self):
        """the url to the Django admin interface for the model instance"""
        from django.urls import reverse
        info = (self._meta.app_label, self._meta.model_name)
        return reverse('admin:%s_%s_change' % info, args=(self.pk,))

# Header API Keys Model.
class APIAuthKey(models.Model):
    key             = models.UUIDField(primary_key=True, default= uuid.uuid4)
    isRevoked       = models.BooleanField(default=False)
    ipaddress       = models.GenericIPAddressField(null=True, blank=True)
    browserinfo     = models.TextField(null=True, blank=True)
    createdAt       = models.DateTimeField(auto_now_add=True)
    updatedAt       = models.DateTimeField(auto_now=True)
    createdBy       = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True)

    def __int__(self):
        return self.id
    def __str__(self):
        return str(self.key)

    class Meta:
        verbose_name = "API Auth Key"
        verbose_name_plural = "API Auth Keys"


class SourceDetails(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    discription = models.TextField(null=True, blank=True)
    image_url = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default = True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    createdBy = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True)

    def __int__(self):
        return self.id
    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Source"
        verbose_name_plural = "Source"