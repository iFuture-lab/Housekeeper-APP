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
from .models import PericePerNationality
from .serializers import PericePerNationalitySerializer
from service_type.models import ServiceType
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

    
class PericePerNationalityRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PericePerNationality.objects.all()
    serializer_class = PericePerNationalitySerializer
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        operation_description="Create a new PericePerNationality",
        responses={
            201: PericePerNationalitySerializer,
            400: 'Bad Request'
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
        
class PericePerNationalityCreateView(generics.ListCreateAPIView):
    queryset = PericePerNationality.objects.all()
    serializer_class = PericePerNationalitySerializer
    permission_classes = [AllowAny]
    
    
    @swagger_auto_schema(
        operation_description="Retrieve a PericePerNationality by ID",
        responses={
            200: PericePerNationalitySerializer,
            404: 'Not Found'
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a PericePerNationality by ID",
        request_body=PericePerNationalitySerializer,
        responses={
            200: PericePerNationalitySerializer,
            400: 'Bad Request',
            404: 'Not Found'
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a PericePerNationality by ID",
        responses={
            204: 'No Content',
            404: 'Not Found'
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs) 
    
    
    