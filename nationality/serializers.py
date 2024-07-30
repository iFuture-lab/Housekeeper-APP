

from rest_framework import serializers

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Nationallity


class NationalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Nationallity
        fields = ['id', 'Nationality']
        
        

