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
    
class RolePerUserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RolePerUser.objects.all()
    serializer_class = RolePerUserSerializer
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        operation_description="Create a new permission",
        responses={
            201: RolePerUserSerializer,
            400: 'Bad Request'
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
        
class RolePerUserCreateView(generics.ListCreateAPIView):
    queryset = RolePerUser.objects.all()
    serializer_class = RolePerUserSerializer
    permission_classes = [AllowAny]
    
    
    @swagger_auto_schema(
        operation_description="Retrieve a Permission by ID",
        responses={
            200: RolePerUserSerializer,
            404: 'Not Found'
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a permission",
        request_body=RolePerUserSerializer,
        responses={
            200: RolePerUserSerializer,
            400: 'Bad Request',
            404: 'Not Found'
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a permission by ID",
        responses={
            204: 'No Content',
            404: 'Not Found'
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs) 
    
    
    
class RolePerClientRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RolePerClient.objects.all()
    serializer_class = RolePerClientSerializer
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        operation_description="Create a new permission",
        responses={
            201: RolePerClientSerializer,
            400: 'Bad Request'
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
        
class RolePerClientCreateView(generics.ListCreateAPIView):
    queryset = RolePerClient.objects.all()
    serializer_class = RolePerClientSerializer
    permission_classes = [AllowAny]
    
    
    @swagger_auto_schema(
        operation_description="Retrieve a Permission by ID",
        responses={
            200: RolePerClientSerializer,
            404: 'Not Found'
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a permission",
        request_body=RolePerClientSerializer,
        responses={
            200: RolePerClientSerializer,
            400: 'Bad Request',
            404: 'Not Found'
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a permission by ID",
        responses={
            204: 'No Content',
            404: 'Not Found'
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs) 
    
    
    
    
    
    