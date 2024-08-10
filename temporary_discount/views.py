from rest_framework import generics, filters
from rest_framework.pagination import PageNumberPagination
from .models import TempoararyDiscount
from .serializers import DiscountSerializer
from django.shortcuts import render
from rest_framework.permissions import AllowAny

# Create your views here.

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

