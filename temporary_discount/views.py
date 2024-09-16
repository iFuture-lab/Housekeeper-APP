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
from housekeeper.permissions import MethodBasedPermissionsMixin

class PackageByRequestTypeView(MethodBasedPermissionsMixin,generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CustomPackageSerializer
    
    def get_queryset(self):
        # Get request_type_id from URL parameters
        request_type_id = self.kwargs.get('request_type_id')

        
        if not request_type_id:
            return CustomPackage.objects.none()

       
        try:
            request_type = ServiceType.objects.get(id=request_type_id)
        except ServiceType.DoesNotExist:
            return CustomPackage.objects.none()

        
        queryset = CustomPackage.objects.filter(request_type=request_type)
        return queryset
    
    
    
class PackageRetrieveUpdateDestroyView(MethodBasedPermissionsMixin,generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomPackage.objects.all()
    serializer_class = CustomPackageSerializer
    permission_classes = [AllowAny]
   
    
    
class PackageCreateView(MethodBasedPermissionsMixin,generics.ListCreateAPIView):
    queryset = CustomPackage.objects.all()
    serializer_class = CustomPackageSerializer
    permission_classes = [AllowAny] 
    
    def perform_create(self, serializer):
        
        serializer.save()
    




class DiscountRetrieveUpdateDestroyView(MethodBasedPermissionsMixin,generics.RetrieveUpdateDestroyAPIView):
    queryset = TempoararyDiscount.objects.all()
    serializer_class = DiscountSerializer
    # permission_classes = [AllowAny]
   
    
    
class DiscountCreateView(MethodBasedPermissionsMixin,generics.ListCreateAPIView):
    queryset = TempoararyDiscount.objects.all()
    serializer_class = DiscountSerializer
    # permission_classes = [AllowAny] 
    
    
class PromotionCodeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TempoararyDiscount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [AllowAny] 
    
    
    
class PromotionCodeCreateView(generics.ListCreateAPIView):
    queryset = TempoararyDiscount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [AllowAny] 

