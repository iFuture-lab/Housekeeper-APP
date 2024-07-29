from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend

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
from .serializer import DummyHousekeeperSerializer,HousekeeperIDSerializer,DummyHireHousekeeperSerializer,DummyRecruitmentRequestSerializer,DummyTransferRequestSerializer,DeleteHousekeeper,UpdateHireRequest
from.models import Status
from .filter import HousekeeperFilter
from django.db import transaction
from .filter import StatusFilter


################################filter for request Status####################################################


class RecruitmentListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = RecruitmentRequest.objects.all()
    serializer_class = HousekeeperSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = StatusFilter

class HireRequestListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = HireRequest.objects.all()
    serializer_class = HireRequestSerializer
    # filter_backends = [DjangoFilterBackend]
    filterset_class = StatusFilter

class TransferRequestListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = TransferRequest.objects.all()
    serializer_class = TransferRequestSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = StatusFilter





###################################filter for nationallity, Age, is_avalibale #################################

class AvailableHousekeeper(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Housekeeper.objects.all()
    serializer_class = HousekeeperSerializer
    filter_backends = [DjangoFilterBackend]
    #filterset_fields = ['is_available', 'nationality','isactive','Age']
    filterset_class = HousekeeperFilter
    
    
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
    
    
    def delete(self, request, *args, **kwargs):
        # Extract the 'ids' parameter from the query parameters
        ids = request.query_params.get('ids', '')

        # Split the 'ids' parameter by commas and convert to integers
        try:
            ids = list(map(int, ids.split(',')))
        except ValueError:
            return Response({"error": "Invalid ID format. Please provide a comma-separated list of integers."}, status=status.HTTP_400_BAD_REQUEST)

        # Delete the Housekeeper objects with the given IDs
        count, _ = HireRequest.objects.filter(id__in=ids).delete()

        # Return the count of deleted objects
        return Response({"deleted": count}, status=status.HTTP_204_NO_CONTENT)
    
class HireRequestListCreateView(generics.ListCreateAPIView):
    queryset = HireRequest.objects.all()
    serializer_class = HireRequestSerializer
    permission_classes = [AllowAny] 

class HireRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HireRequest.objects.all()
    serializer_class = HireRequestSerializer
    permission_classes = [AllowAny] 
    
    
########## updating ################################
class HousekeeperBatchStatusUpdateView(APIView):
    serializer_class= UpdateHireRequest
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'ids',
                openapi.IN_QUERY,
                description="Comma-separated list of IDs",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'status',
                openapi.IN_QUERY,
                description="New status value",
                type=openapi.TYPE_STRING
            ),
        ]
    )
    
    
    @transaction.atomic 
    def patch(self, request, *args, **kwargs):
        # Extract the 'ids' and 'status' parameters from the query parameters
        ids = request.query_params.get('ids', '')
        new_status_name = request.query_params.get('status', '')

        # Split the 'ids' parameter by commas and convert to integers
        try:
            ids = list(map(int, ids.split(',')))
        except ValueError:
            return Response({"error": "Invalid ID format. Please provide a comma-separated list of integers."}, status=status.HTTP_400_BAD_REQUEST)

        if not new_status_name:
            return Response({"error": "Status value is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the Status object based on the provided status name
        try:
            new_status = Status.objects.get(Status=new_status_name)
        except Status.DoesNotExist:
            return Response({"error": f"Status '{new_status_name}' does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Query the Housekeeper objects with the given IDs
        housekeepers = HireRequest.objects.filter(id__in=ids)
        if not housekeepers.exists():
            return Response({"error": "No Hire Requests found for the provided IDs."}, status=status.HTTP_404_NOT_FOUND)

        # Update the status field for the queried Housekeeper objects
        housekeepers.update(status=new_status)
        # Update Status and Housekeeper Availability
        for hire_request in housekeepers:
            hire_request.status = new_status
            hire_request.save()  # Save to trigger the update

            if new_status.Status == "Approved":
                housekeeper = hire_request.housekeeper
                housekeeper.is_available = False
                housekeeper.save()
            else:
                housekeeper = hire_request.housekeeper
                housekeeper.is_available = True
                housekeeper.save()
                
                
                         
        
        return Response({"message": "Status updated successfully."}, status=status.HTTP_200_OK)
     
        
    
    
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
    
    
    def delete(self, request, *args, **kwargs):
        # Extract the 'ids' parameter from the query parameters
        ids = request.query_params.get('ids', '')

        # Split the 'ids' parameter by commas and convert to integers
        try:
            ids = list(map(int, ids.split(',')))
        except ValueError:
            return Response({"error": "Invalid ID format. Please provide a comma-separated list of integers."}, status=status.HTTP_400_BAD_REQUEST)

        # Delete the Housekeeper objects with the given IDs
        count, _ = RecruitmentRequest.objects.filter(id__in=ids).delete()

        # Return the count of deleted objects
        return Response({"deleted": count}, status=status.HTTP_204_NO_CONTENT)
    

    

class RecruitmentRequestListCreateView(generics.ListCreateAPIView):
    queryset = RecruitmentRequest.objects.all()
    serializer_class = RecruitmentRequestSerializer
    permission_classes = [AllowAny] 

class RecruitmentRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RecruitmentRequest.objects.all()
    serializer_class = RecruitmentRequestSerializer
    permission_classes = [AllowAny] 
    
    
    ########## updating ################################
class RecruitmentBatchStatusUpdateView(APIView):
    serializer_class= UpdateHireRequest
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'ids',
                openapi.IN_QUERY,
                description="Comma-separated list of IDs",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'status',
                openapi.IN_QUERY,
                description="New status value",
                type=openapi.TYPE_STRING
            ),
        ]
    )
    
    @transaction.atomic
    def patch(self, request, *args, **kwargs):
        # Extract the 'ids' and 'status' parameters from the query parameters
        ids = request.query_params.get('ids', '')
        new_status_name = request.query_params.get('status', '')

        # Split the 'ids' parameter by commas and convert to integers
        try:
            ids = list(map(int, ids.split(',')))
        except ValueError:
            return Response({"error": "Invalid ID format. Please provide a comma-separated list of integers."}, status=status.HTTP_400_BAD_REQUEST)

        if not new_status_name:
            return Response({"error": "Status value is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the Status object based on the provided status name
        try:
            new_status = Status.objects.get(Status=new_status_name)
        except Status.DoesNotExist:
            return Response({"error": f"Status '{new_status_name}' does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Query the Housekeeper objects with the given IDs
        Recruitment = RecruitmentRequest.objects.filter(id__in=ids)

        if not Recruitment.exists():
            return Response({"error": "No Recruitment Requests found for the provided IDs."}, status=status.HTTP_404_NOT_FOUND)

        # Update the status field for the queried Housekeeper objects
        Recruitment.update(status=new_status)
        for hire_request in Recruitment:
            hire_request.status = new_status
            hire_request.save()  # Save to trigger the update

            if new_status.Status == "Approved":
                housekeeper = hire_request.housekeeper
                housekeeper.is_available = False
                housekeeper.save()
            else:
                housekeeper = hire_request.housekeeper
                housekeeper.is_available = True
                housekeeper.save()
                   
        return Response({"message": "Status updated successfully."}, status=status.HTTP_200_OK)
        
    
    
    
    
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
    
    
    def delete(self, request, *args, **kwargs):
        # Extract the 'ids' parameter from the query parameters
        ids = request.query_params.get('ids', '')

        # Split the 'ids' parameter by commas and convert to integers
        try:
            ids = list(map(int, ids.split(',')))
        except ValueError:
            return Response({"error": "Invalid ID format. Please provide a comma-separated list of integers."}, status=status.HTTP_400_BAD_REQUEST)

        # Delete the Housekeeper objects with the given IDs
        count, _ = TransferRequest.objects.filter(id__in=ids).delete()

        # Return the count of deleted objects
        return Response({"deleted": count}, status=status.HTTP_204_NO_CONTENT)
    
    
    
    
class TransferRequestListCreateView(generics.ListCreateAPIView):
    queryset = TransferRequest.objects.all()
    serializer_class = TransferRequestSerializer
    permission_classes = [AllowAny] 

class TransferRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TransferRequest.objects.all()
    serializer_class = TransferRequestSerializer
    permission_classes = [AllowAny] 
    

    
class TransferBatchStatusUpdateView(APIView):
    serializer_class= UpdateHireRequest
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'ids',
                openapi.IN_QUERY,
                description="Comma-separated list of IDs",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'status',
                openapi.IN_QUERY,
                description="New status value",
                type=openapi.TYPE_STRING
            ),
        ]
    )
    
    @transaction.atomic
    def patch(self, request, *args, **kwargs):
        # Extract the 'ids' and 'status' parameters from the query parameters
        ids = request.query_params.get('ids', '')
        new_status_name = request.query_params.get('status', '')

        # Split the 'ids' parameter by commas and convert to integers
        try:
            ids = list(map(int, ids.split(',')))
        except ValueError:
            return Response({"error": "Invalid ID format. Please provide a comma-separated list of integers."}, status=status.HTTP_400_BAD_REQUEST)

        if not new_status_name:
            return Response({"error": "Status value is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the Status object based on the provided status name
        try:
            new_status = Status.objects.get(Status=new_status_name)
        except Status.DoesNotExist:
            return Response({"error": f"Status '{new_status_name}' does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Query the Housekeeper objects with the given IDs
        Transfer = TransferRequest.objects.filter(id__in=ids)

        if not Transfer.exists():
            return Response({"error": "No Transfer Requests found for the provided IDs."}, status=status.HTTP_404_NOT_FOUND)

        # Update the status field for the queried Housekeeper objects
        Transfer.update(status=new_status)
        
        for hire_request in Transfer:
            hire_request.status = new_status
            hire_request.save()  # Save to trigger the update

            if new_status.Status == "Approved":
                housekeeper = hire_request.housekeeper
                housekeeper.is_available = False
                housekeeper.save()
            else:
                housekeeper = hire_request.housekeeper
                housekeeper.is_available = True
                housekeeper.save()
        
        return Response({"message": "Status updated successfully."}, status=status.HTTP_200_OK)
        
    
    
    
    

