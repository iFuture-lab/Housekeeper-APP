from rest_framework import serializers
from .models import Role,Permission
from django.contrib.auth.models import User
from login.serializers import RegisterSerializer


class PermissioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissioSerializer(many=True)
    class Meta:
        model = Role
        fields = '__all__'

class PermissionSerializer(serializers.Serializer):
    permissions = serializers.ListField(allow_empty=True)
    user = serializers.IntegerField(write_only=True)
    user_detail = RegisterSerializer(read_only=True, source='user')

    def create(self, validated_data):
        return {
            'permissions': validated_data['permissions'],
            'user': validated_data['user'],
        }
    
    class Meta:
        model = Permission
        fields = ['permissions', 'user_detail']