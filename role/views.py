from django.shortcuts import render
from .serializers import RoleSerializer,PermissioSerializer, PermissionSerializer
from rest_framework import generics, filters, pagination
from .models import Role
from django.contrib.auth.models import Permission
from rest_framework.permissions import AllowAny
from housekeeper.permissions import MethodBasedPermissionsMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from login.serializers import RegisterSerializer

# Create your views here.


class RoleCreateView(MethodBasedPermissionsMixin,generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    # permission_classes = [AllowAny]
    
    
class RoleDetailView(MethodBasedPermissionsMixin,generics.RetrieveAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    # permission_classes = [AllowAny]
    
    
    
class PermissionCreateView(MethodBasedPermissionsMixin,generics.ListCreateAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    # permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        perms = [{'user': user.id, 'user_detail': RegisterSerializer(user).data, 'permissions': list(sorted(user.user_permissions.values_list('codename', flat=True)))} for user in users]
        return Response(perms)
    
    def post(self, request):
        serializer = PermissionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = serializer.validated_data['user']
        user = User.objects.filter(id=user_id)
        if user.exists():
            user = user.first()
        else:
            return Response({'detail': 'User not found'}, status=404)
        perms = Permission.objects.filter(codename__in=serializer.validated_data['permissions'])
        if not len(perms) == len(serializer.validated_data['permissions']):
        # if (not perms.exists() and serializer.validated_data['permissions'] != []) or (serializer.validated_data['permissions'] == []):
            return Response({'detail': 'Invalid permissions format. Provide a list of permissions in the format ["{action}_{model}"] or []'}, status=400)
        user.user_permissions.set(perms)
        return Response({'detail': 'Permissions saved successfully'})
