from rest_framework import serializers

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import ServiceType


class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = ['id', 'name']
        
        


        
        

