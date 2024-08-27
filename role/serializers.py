from rest_framework import serializers
from .models import Role,Permission


        
        

        
        
class PermissioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'
        
class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissioSerializer(many=True)
    class Meta:
        model = Role
        fields = '__all__'