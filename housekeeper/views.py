from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Housekeeper, HireRequest, RecruitmentRequest, TransferRequest
from .serializer import HousekeeperSerializer, HireRequestSerializer, RecruitmentRequestSerializer, TransferRequestSerializer

class HousekeeperListCreateView(generics.ListCreateAPIView):
    queryset = Housekeeper.objects.all()
    serializer_class = HousekeeperSerializer
    permission_classes = [AllowAny] 

class HousekeeperDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Housekeeper.objects.all()
    serializer_class = HousekeeperSerializer
    permission_classes = [AllowAny] 
    
    
class HousekeeperIDsView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        housekeepers = Housekeeper.objects.values_list('id', flat=True)
        return Response(housekeepers, status=status.HTTP_200_OK)

class HireRequestListCreateView(generics.ListCreateAPIView):
    queryset = HireRequest.objects.all()
    serializer_class = HireRequestSerializer
    permission_classes = [AllowAny] 

class HireRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HireRequest.objects.all()
    serializer_class = HireRequestSerializer
    permission_classes = [AllowAny] 

class RecruitmentRequestListCreateView(generics.ListCreateAPIView):
    queryset = RecruitmentRequest.objects.all()
    serializer_class = RecruitmentRequestSerializer
    permission_classes = [AllowAny] 

class RecruitmentRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RecruitmentRequest.objects.all()
    serializer_class = RecruitmentRequestSerializer
    permission_classes = [AllowAny] 

class TransferRequestListCreateView(generics.ListCreateAPIView):
    queryset = TransferRequest.objects.all()
    serializer_class = TransferRequestSerializer
    permission_classes = [AllowAny] 

class TransferRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TransferRequest.objects.all()
    serializer_class = TransferRequestSerializer
    permission_classes = [AllowAny] 
