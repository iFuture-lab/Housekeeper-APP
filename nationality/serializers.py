

from rest_framework import serializers

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Nationallity


class NationalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Nationallity
        fields = ['id', 'Nationality']
        
        
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('deleted_at', None)
        
        

