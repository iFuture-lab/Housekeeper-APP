from rest_framework import serializers
from .models import RolePerUser,RolePerClient

class RolePerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolePerUser
        fields = '__all__'


class RolePerClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolePerClient
        fields = '__all__'
        
        
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolePerClient
        fields = '__all__'
        
        
class PermissioSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolePerClient
        fields = '__all__'