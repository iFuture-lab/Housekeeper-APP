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
    
  
        
class PericePerNationalityCreateView(generics.ListCreateAPIView):
    queryset = PericePerNationality.objects.all()
    serializer_class = PericePerNationalitySerializer
    permission_classes = [AllowAny]
    
    
  
    
    
    