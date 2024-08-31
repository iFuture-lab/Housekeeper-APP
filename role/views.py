from django.shortcuts import render
from .serializers import RoleSerializer,PermissioSerializer
from rest_framework import generics, filters
from .models import Role, Permission
from rest_framework.permissions import AllowAny
from housekeeper.permissions import MethodBasedPermissionsMixin

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
    serializer_class = PermissioSerializer
    # permission_classes = [AllowAny]