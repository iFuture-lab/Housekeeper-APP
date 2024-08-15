from django.shortcuts import render
from .serializers import RoleSerializer,PermissioSerializer
from rest_framework import generics, filters
from .models import Role
from rest_framework.permissions import AllowAny

# Create your views here.


class RoleCreateView(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [AllowAny]