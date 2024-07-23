from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from dj_rest_auth.serializers import LoginSerializer as DjLoginSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser




class RegisterSerializercustomer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        ref_name = 'RegisterSerializercustomer'  # Explicitly set ref_name
        model = CustomUser
        fields = ('username', 'password', 'password2','phone_number','first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'phone_number': {'required': True}
        }
        
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            phone_number=validated_data['phone_number'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        return user





class LoginSerializercustomer(serializers.Serializer):
 
    username=serializers.CharField()
    phone_number = serializers.CharField()
    password = serializers.CharField()
   
    
    
    class Meta:
        ref_name = 'LoginSerializercustomer'  # Explicitly set ref_name
        
        
        
        
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        ref_name = 'RegisterSerializer'  # Explicitly set ref_name
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
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
    


# class LoginSerializer(DjLoginSerializer):
#     class Meta:
#         ref_name = "DjLoginSerializer"  # Set a unique ref_name


class LoginSerializer(serializers.Serializer):
    username= serializers.CharField() 
    email= serializers.CharField()
    password = serializers.CharField()
    

    class Meta:
        ref_name = 'LoginSerializer'  # Explicitly set ref_name