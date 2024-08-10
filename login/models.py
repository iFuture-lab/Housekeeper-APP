from django.db import models
# from django.contrib.auth.models import User
#from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from role.models import Role
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone
from django.conf import settings
import uuid


# Create your models here.# login/models.py



######################## token#################################
class BlacklistedToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.token
############ User model for Customers #########################

class CustomUserManager(BaseUserManager):
    def create_user(self, fullName, phone_number, password=None, password2=None, **extra_fields):
        if not fullName:
            raise ValueError('The fullName field must be set')
        if not phone_number:
            raise ValueError('The Phone number field must be set')

        user = self.model(fullName=fullName, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        # user.set_password(password2)
        user.save(using=self._db)
        return user

    def create_superuser(self, fullName, phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(fullName, phone_number, password, **extra_fields)



class CustomUser(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fullName = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)  # Ensure you hash passwords properly
    # password2 = models.CharField(max_length=128)  # Ensure you hash passwords properly
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True,unique=True) # Validators should be a list
    email=models.CharField(max_length=100)
    dateOfBirth = models.DateField(default=timezone.now) 
    nationalID=  models.CharField(max_length=100,default="1234567890o")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
     
    USERNAME_FIELD = 'fullName'
    REQUIRED_FIELDS = ['phone_number']

    objects = CustomUserManager()

    def __str__(self):
        return self.fullName
    
    
    
class OtpMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    body = models.TextField()
    is_active = models.BooleanField(default=True)
    

    
    
    

        
############### System Users############################
    
# class User(models.Model):
    
#     # def get_default_role():
#     #     return Role.objects.get(name='admin')

#     username = models.CharField(max_length=150, unique=True)
#     password = models.CharField(max_length=128)  # Ensure you hash passwords properly
#     password2 = models.CharField(max_length=128)  # Ensure you hash passwords properly
#     email = models.EmailField(unique=True)
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#     role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)  # Add role field
    
#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = []


#     def __str__(self):
#         return self.username

    

    
    
    
    