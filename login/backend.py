from django.contrib.auth.backends import BaseBackend
from .models import CustomUser  # Import your custom user model
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

# UserModel = get_user_model()
# User=CustomUser

##########################django by default authenticate with username this function use phonenumber as authentication methods ###################################################
class PhoneNumberBackend(BaseBackend):
    def authenticate(self, request, phone_number=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(phone_number=phone_number)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None
    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
