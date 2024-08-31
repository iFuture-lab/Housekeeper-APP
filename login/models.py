from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from role.models import Role
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone
from django.conf import settings
import uuid
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from datetime import date





######################### soft delteing ##################################

class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        #  filters out soft-deleted records
        return super().get_queryset().filter(deleted_at__isnull=True)

    def deleted(self):
        # Return only soft-deleted records
        return super().get_queryset().filter(deleted_at__isnull=False)

    def with_deleted(self):
        # all the records 
        return super().get_queryset()



######################## token#################################
class BlacklistedToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    objects = SoftDeleteManager()  # Custom manager
    all_objects = models.Manager()  # Default manager to access all records, including deleted

    def delete(self):
       #soft deleting
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        # Restore a soft-deleted record 
        self.deleted_at = None
        self.save()

    def hard_delete(self):
        # delete the record in real 
        super().delete()

    def __str__(self):
        return self.token
############ User model for Customers(mobile users) #########################

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
    
    
    
    
def validate_saudi_national_id(value):
    if len(value) != 10:
        raise ValidationError('National ID must be 10 digits long.')
    if not value.isdigit():
        raise ValidationError('National ID must be only Numbers.')




class CustomUser(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fullName = models.CharField(max_length=150)
    password = models.CharField(max_length=128)  # ensure to hash password properly
    # password2 = models.CharField(max_length=128)  
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True,unique=True) 
    email=models.CharField(max_length=100,null=True, validators=[EmailValidator(message="Enter a valid email address.")],blank=True)
    dateOfBirth = models.DateField(default=timezone.now) 
    # nationalID=  models.CharField(max_length=100,validators=[validate_saudi_national_id])
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_confirmed= models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
     
    USERNAME_FIELD = 'fullName'
    REQUIRED_FIELDS = ['phone_number']

    objects = CustomUserManager()
    
    soft_deleted = SoftDeleteManager()
    all_objects = models.Manager()  
    def delete(self):
       #soft deleting
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        # Restore a soft-deleted record 
        self.deleted_at = None
        self.save()

    def hard_delete(self):
        # delete the record in real 
        super().delete()

    def __str__(self):
        return self.fullName
    
    
    # def clean(self):
    #     super().clean()
    #     if self.dateOfBirth > date.today():
    #         raise ValidationError('Date of birth cannot be in the future.')

    # def save(self, *args, **kwargs):
    #     self.full_clean()  # Ensure validation is performed before saving
    #     super().save(*args, **kwargs)
        
        
    
    
################################## this model to store the otp messaage in database #############################################################
    
class OtpMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    body = models.TextField()
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    objects = SoftDeleteManager()  
    all_objects = models.Manager()  

    def delete(self):
       #soft deleting
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        # Restore a soft-deleted record 
        self.deleted_at = None
        self.save()

    def hard_delete(self):
        # delete the record in real 
        super().delete()

    def __str__(self):
        return self.name
    

    
    
    

        
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

    

    
    
    
    