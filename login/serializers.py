from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from dj_rest_auth.serializers import LoginSerializer as DjLoginSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from django.contrib.auth import get_user_model
# from .models import User
from django.contrib.auth.tokens import default_token_generator

from django.contrib.auth import get_user_model

User = get_user_model()
from .utils import send_otp, verify_otp


# UserModel = get_user_model()


####################################Admin Reset Password#############################

class AdminPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            self.user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError(_('User with this email does not exist.'))
        return value

    def save(self):
        token = default_token_generator.make_token(self.user)
        # Send this token to the user via email
        # Example: send_email(self.user.email, f'Your reset token is {token}')
        return token

class AdminPasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        self.user = User.objects.get(email=attrs['email'])
        if not default_token_generator.check_token(self.user, attrs['token']):
            raise serializers.ValidationError(_('Invalid token or expired.'))
        return attrs

    def save(self):
        self.user.set_password(self.validated_data['new_password'])
        self.user.save()


###########################Clients##################################################

class PasswordResetSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    def validate_phone_number(self, value):
        try:
            self.user = CustomUser.objects.get(phone_number=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(_('User with this phone number does not exist.'))
        return value

    def save(self):
        token = default_token_generator.make_token(self.user)
        # You can send this token via SMS to the user's phone number
        return token
    
class PasswordResetConfirmSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        self.user = CustomUser.objects.get(phone_number=attrs['phone_number'])
        if not default_token_generator.check_token(self.user, attrs['token']):
            raise serializers.ValidationError(_('Invalid token or expired.'))
        return attrs

    def save(self):
        self.user.set_password(self.validated_data['new_password'])
        self.user.save()
    
    
    
    ##################################################################################################
    



class RegisterSerializercustomer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    #otp = serializers.CharField(write_only=True, required=True)


    class Meta:
        ref_name = 'RegisterSerializercustomer'  # Explicitly set ref_name
        model = CustomUser
        #model = UserModel
        fields = ('fullName','phone_number','password','password2','dateOfBirth', 'nationalID','email')
        extra_kwargs = {
            'dateOfBirth': {'required': True},
            'nationalID': {'required': True},
            'phone_number': {'required': True},
            'fullName': {'required': True}
            
        }
        
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        # Verify OTP
        # if not verify_otp(attrs['phone_number'], attrs['otp']):
        #     raise serializers.ValidationError({"otp": "Invalid or expired OTP."})
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            fullName=validated_data['fullName'],
            phone_number=validated_data['phone_number'],
            nationalID=validated_data['nationalID'],
            dateOfBirth=validated_data['dateOfBirth'],
            password=validated_data['password'],
            email=validated_data['email'],
        )
        return user





class LoginSerializercustomer(serializers.Serializer):
 
    # username=serializers.CharField()
    phone_number = serializers.CharField()
    password = serializers.CharField()
   
    
    def validate(self, data):
        phone_number = data.get('phone_number')
        password = data.get('password')

        if not phone_number or not password:
            raise serializers.ValidationError("Phone number and password are required")

        user = authenticate(phone_number=phone_number, password=password)

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        data['user'] = user
        return data
    
    class Meta:
        ref_name = 'LoginSerializercustomer'  # Explicitly set ref_name
        
        
        
        
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        ref_name = 'RegisterSerializer'  # Explicitly set ref_name
        model = User
        fields = ('username', 'password','password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    


class LoginSerializer(serializers.Serializer):
    username= serializers.CharField() 
    password = serializers.CharField()
    
    def validate(self, data):
        #email = data.get('email')
        username = data.get('username')
        password = data.get('password')

        if not password:
            raise serializers.ValidationError("Must include password")


        user = authenticate(
            request=self.context.get('request'),
            username=username,
            # email=email,
            password=password
        )

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        data['user'] = user
        return data
    
    class Meta:
        ref_name = 'LoginSerializer'  