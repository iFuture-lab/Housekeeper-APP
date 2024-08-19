from rest_framework import generics, filters
from rest_framework.pagination import PageNumberPagination
from .models import TempoararyDiscount
from .serializers import DiscountSerializer
from django.shortcuts import render
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework import status
from .models import CustomPackage
from .serializers import CustomPackageSerializer
from service_type.models import ServiceType

class PackageByRequestTypeView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CustomPackageSerializer
    
    def get_queryset(self):
        # Get request_type_id from URL parameters
        request_type_id = self.kwargs.get('request_type_id')

        # Check if request_type_id is present
        if not request_type_id:
            return CustomPackage.objects.none()

        # Validate request_type_id and retrieve ServiceType
        try:
            request_type = ServiceType.objects.get(id=request_type_id)
        except ServiceType.DoesNotExist:
            return CustomPackage.objects.none()

        # Filter CustomPackage objects based on the request_type
        queryset = CustomPackage.objects.filter(request_type=request_type)
        return queryset
    
    
    
class PackageRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomPackage.objects.all()
    serializer_class = CustomPackageSerializer
    permission_classes = [AllowAny]
   
    
    
class PackageCreateView(generics.ListCreateAPIView):
    queryset = CustomPackage.objects.all()
    serializer_class = CustomPackageSerializer
    permission_classes = [AllowAny] 
    
    def perform_create(self, serializer):
        # The serializer will handle the creation of the CustomPackage
        serializer.save()
    




class DiscountRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TempoararyDiscount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [AllowAny]
   
    
    
class DiscountCreateView(generics.ListCreateAPIView):
    queryset = TempoararyDiscount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [AllowAny] 
    
    
class PromotionCodeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TempoararyDiscount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [AllowAny] 
    
    
    
class PromotionCodeCreateView(generics.ListCreateAPIView):
    queryset = TempoararyDiscount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [AllowAny] 

