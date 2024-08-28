from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, filters
from rest_framework.pagination import PageNumberPagination
# from .models import TempoararyDiscount
# from .serializers import DiscountSerializer
from django.shortcuts import render
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework import status
from .models import RolePerUser,RolePerClient
from service_type.models import ServiceType
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import RolePerUserSerializer,RolePerClientSerializer
from housekeeper.permissions import MethodBasedPermissionsMixin
    
class RolePerUserRetrieveUpdateDestroyView(MethodBasedPermissionsMixin,generics.RetrieveUpdateDestroyAPIView):
    queryset = RolePerUser.objects.all()
    serializer_class = RolePerUserSerializer
    # permission_classes = [AllowAny]
 
    
        
class RolePerUserCreateView(MethodBasedPermissionsMixin,generics.ListCreateAPIView):
    queryset = RolePerUser.objects.all()
    serializer_class = RolePerUserSerializer
    # permission_classes = [AllowAny]
    
    

  
    
    
    
class RolePerClientRetrieveUpdateDestroyView(MethodBasedPermissionsMixin,generics.RetrieveUpdateDestroyAPIView):
    queryset = RolePerClient.objects.all()
    serializer_class = RolePerClientSerializer
    # permission_classes = [AllowAny]

    
        
class RolePerClientCreateView(MethodBasedPermissionsMixin,generics.ListCreateAPIView):
    queryset = RolePerClient.objects.all()
    serializer_class = RolePerClientSerializer
    # permission_classes = [AllowAny]
    

    
    
    
    
    
    