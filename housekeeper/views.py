from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .models import Housekeeper, HireRequest, RecruitmentRequest, TransferRequest
from .serializer import HousekeeperSerializer, HireRequestSerializer, RecruitmentRequestSerializer, TransferRequestSerializer
from .serializer import DummyHousekeeperSerializer,HousekeeperIDSerializer,DummyHireHousekeeperSerializer,DummyRecruitmentRequestSerializer,DummyTransferRequestSerializer,DeleteHousekeeper

class HousekeeperBatchDetailView(APIView):
    permission_classes = [AllowAny]
    serializer_class = DummyHousekeeperSerializer
     
    @swagger_auto_schema(
         manual_parameters=[
             openapi.Parameter(
                'ids',
                openapi.IN_QUERY,
                description="Comma-separated list of IDs",
                type=openapi.TYPE_STRING
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        # Extract the 'ids' parameter from the query parameters
        ids = request.query_params.get('ids', '')

        # Split the 'ids' parameter by commas and convert to integers
        try:
            ids = list(map(int, ids.split(',')))
        except ValueError:
            return Response({"error": "Invalid ID format. Please provide a comma-separated list of integers."}, status=status.HTTP_400_BAD_REQUEST)

        # Query the Housekeeper objects with the given IDs
        housekeepers = Housekeeper.objects.filter(id__in=ids)

        # Serialize the data
        serializer = HousekeeperSerializer(housekeepers, many=True)
        
        # Return the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class HousekeeperBatchDeleteView(APIView):
    permission_classes = [AllowAny]
    serilaizer_class= DeleteHousekeeper

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'ids',
                openapi.IN_QUERY,
                description="Comma-separated list of IDs to delete",
                type=openapi.TYPE_STRING
            )
        ],
        responses={204: 'No Content'}
    )
    def delete(self, request, *args, **kwargs):
        # Extract the 'ids' parameter from the query parameters
        ids = request.query_params.get('ids', '')

        # Split the 'ids' parameter by commas and convert to integers
        try:
            ids = list(map(int, ids.split(',')))
        except ValueError:
            return Response({"error": "Invalid ID format. Please provide a comma-separated list of integers."}, status=status.HTTP_400_BAD_REQUEST)

        # Delete the Housekeeper objects with the given IDs
        count, _ = Housekeeper.objects.filter(id__in=ids).delete()

        # Return the count of deleted objects
        return Response({"deleted": count}, status=status.HTTP_204_NO_CONTENT)


class HousekeeperListCreateView(generics.ListCreateAPIView):
    queryset = Housekeeper.objects.all()
    serializer_class = HousekeeperSerializer
    permission_classes = [AllowAny] 

class HousekeeperDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Housekeeper.objects.all()
    serializer_class = HousekeeperSerializer
    permission_classes = [AllowAny] 


    
class HousekeeperIDsView(generics.GenericAPIView):
    serializer_class= HousekeeperIDSerializer
    def get(self, request, *args, **kwargs):
        housekeepers = Housekeeper.objects.values_list('id', flat=True)
        return Response(housekeepers, status=status.HTTP_200_OK)
    
    
#########################################################################################################

class HireHousekeeperBatchDetailView(APIView):
    permission_classes = [AllowAny]
    serializer_class = DummyHireHousekeeperSerializer
     
    @swagger_auto_schema(
         manual_parameters=[
             openapi.Parameter(
                'ids',
                openapi.IN_QUERY,
                description="Comma-separated list of IDs",
                type=openapi.TYPE_STRING
            )
        ]
    )
    
    def get(self, request, *args, **kwargs):
        # Extract the 'ids' parameter from the query parameters
        ids = request.query_params.get('ids', '')

        # Split the 'ids' parameter by commas and convert to integers
        try:
            ids = list(map(int, ids.split(',')))
        except ValueError:
            return Response({"error": "Invalid ID format. Please provide a comma-separated list of integers."}, status=status.HTTP_400_BAD_REQUEST)

        # Query the Housekeeper objects with the given IDs
        housekeepers = HireRequest.objects.filter(id__in=ids)

        # Serialize the data
        serializer = HireRequestSerializer(housekeepers, many=True)
        
        # Return the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class HireRequestListCreateView(generics.ListCreateAPIView):
    queryset = HireRequest.objects.all()
    serializer_class = HireRequestSerializer
    permission_classes = [AllowAny] 

class HireRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HireRequest.objects.all()
    serializer_class = HireRequestSerializer
    permission_classes = [AllowAny] 
    
    
################################################################################

class RecruitmentRequestBatchDetailView(APIView):
    permission_classes = [AllowAny]
    serializer_class = DummyRecruitmentRequestSerializer
     
    @swagger_auto_schema(
         manual_parameters=[
             openapi.Parameter(
                'ids',
                openapi.IN_QUERY,
                description="Comma-separated list of IDs",
                type=openapi.TYPE_STRING
            )
        ]
    )
    
    def get(self, request, *args, **kwargs):
        # Extract the 'ids' parameter from the query parameters
        ids = request.query_params.get('ids', '')

        # Split the 'ids' parameter by commas and convert to integers
        try:
            ids = list(map(int, ids.split(',')))
        except ValueError:
            return Response({"error": "Invalid ID format. Please provide a comma-separated list of integers."}, status=status.HTTP_400_BAD_REQUEST)

        # Query the Housekeeper objects with the given IDs
        housekeepers = RecruitmentRequest.objects.filter(id__in=ids)

        # Serialize the data
        serializer = RecruitmentRequestSerializer(housekeepers, many=True)
        
        # Return the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class RecruitmentRequestListCreateView(generics.ListCreateAPIView):
    queryset = RecruitmentRequest.objects.all()
    serializer_class = RecruitmentRequestSerializer
    permission_classes = [AllowAny] 

class RecruitmentRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RecruitmentRequest.objects.all()
    serializer_class = RecruitmentRequestSerializer
    permission_classes = [AllowAny] 
    
    
    
########################################################################################################


class TransferRequestBatchDetailView(APIView):
    permission_classes = [AllowAny]
    serializer_class = DummyTransferRequestSerializer
     
    @swagger_auto_schema(
         manual_parameters=[
             openapi.Parameter(
                'ids',
                openapi.IN_QUERY,
                description="Comma-separated list of IDs",
                type=openapi.TYPE_STRING
            )
        ]
    )
    
    def get(self, request, *args, **kwargs):
        # Extract the 'ids' parameter from the query parameters
        ids = request.query_params.get('ids', '')

        # Split the 'ids' parameter by commas and convert to integers
        try:
            ids = list(map(int, ids.split(',')))
        except ValueError:
            return Response({"error": "Invalid ID format. Please provide a comma-separated list of integers."}, status=status.HTTP_400_BAD_REQUEST)

        # Query the Housekeeper objects with the given IDs
        housekeepers = TransferRequest.objects.filter(id__in=ids)

        # Serialize the data
        serializer = TransferRequestSerializer(housekeepers, many=True)
        
        # Return the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class TransferRequestListCreateView(generics.ListCreateAPIView):
    queryset = TransferRequest.objects.all()
    serializer_class = TransferRequestSerializer
    permission_classes = [AllowAny] 

class TransferRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TransferRequest.objects.all()
    serializer_class = TransferRequestSerializer
    permission_classes = [AllowAny] 
