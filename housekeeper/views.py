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
from rest_framework.permissions import IsAuthenticated
from .utils import ActionLoggingMixin,send_message
from uuid import UUID




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
    
    
class HousekeeperBatchDetailView(ActionLoggingMixin,APIView):
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
            # ids = list(map(int, ids.split(',')))
            uuid_list = [UUID(id_str) for id_str in ids.split(',')]
        except ValueError:
            self.log_action(
                user=request.user if request.user.is_authenticated else None,
                action_type="Error",
                model_name="Housekeeper",
                description="Invalid ID format in get request"
            )
            return Response({"error": "Invalid ID format. Please provide a comma-separated list of integers."}, status=status.HTTP_400_BAD_REQUEST)

        # Query the Housekeeper objects with the given IDs
        housekeepers = Housekeeper.objects.filter(id__in=uuid_list)

        # Serialize the data
        serializer = HousekeeperSerializer(housekeepers, many=True)
        
        
        
        # Return the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'uuid_list',
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
            # ids = list(map(int, ids.split(',')))
            uuid_list = [UUID(id_str) for id_str in ids.split(',')]
        except ValueError:
            self.log_action(
                user=request.user if request.user.is_authenticated else None,
                action_type="Error",
                model_name="Housekeeper",
                description="Invalid ID format in delete request"
            )
            return Response({"error": "Invalid ID format. Please provide a comma-separated list of integers."}, status=status.HTTP_400_BAD_REQUEST)

        # Delete the Housekeeper objects with the given IDs
        count, _ = Housekeeper.objects.filter(id__in=uuid_list).delete()
        self.log_action(
            user=request.user if request.user.is_authenticated else None,
            action_type="Deleted",
            model_name="Housekeeper",
            description=f"Successfully deleted {count} Housekeeper for IDs: {uuid_list}"
        )

        # Return the count of deleted objects
        return Response({"deleted": count}, status=status.HTTP_204_NO_CONTENT)
    


class HousekeeperListCreateView(ActionLoggingMixin,generics.ListCreateAPIView):
    queryset = Housekeeper.objects.all()
    serializer_class = HousekeeperSerializer
    permission_classes = [AllowAny] 
    
    
    def get(self, request, *args, **kwargs):
        # Log the action  
        user = request.user if request.user.is_authenticated else None
        self.log_action(
            user=user,
            action_type="Listed",
            model_name="Housekeeper"
        )
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Log the action
        user = request.user if request.user.is_authenticated else None
        self.log_action(
            user=user,
            action_type="Created",
            model_name="Housekeeper"
        )
        return super().post(request, *args, **kwargs)

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

class HireHousekeeperBatchDetailView(ActionLoggingMixin,APIView):
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
            # ids = list(map(int, ids.split(',')))
            uuid_list = [UUID(id_str) for id_str in ids.split(',')]
        except ValueError:
            self.log_action(
            user=request.user if request.user.is_authenticated else None,
            action_type="Error",
            model_name="HireReguest",
            description="Invalid ID format in request"
            )
            return Response({"error": "Invalid ID format. Please provide a comma-separated list of integers."}, status=status.HTTP_400_BAD_REQUEST)

        # Query the Housekeeper objects with the given IDs
        housekeepers = HireRequest.objects.filter(id__in=uuid_list)

        # Serialize the data
        serializer = HireRequestSerializer(housekeepers, many=True)
        self.log_action(
        user=request.user if request.user.is_authenticated else None,
        action_type="Retrieved",
        model_name="HireReguest",
        description=f"Successfully retrieved {len(housekeepers)} HireRequests for IDs: {uuid_list}"
    )
        
        
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
            # ids = list(map(int, ids.split(',')))
            uuid_list = [UUID(id_str) for id_str in ids.split(',')]
        except ValueError:
            self.log_action(
            user=request.user if request.user.is_authenticated else None,
            action_type="Error",
            model_name="HireRequest",
            description="Invalid ID format in request"
            )
            return Response({"error": "Invalid ID format. Please provide a comma-separated list of integers."}, status=status.HTTP_400_BAD_REQUEST)

        # Delete the Housekeeper objects with the given IDs
        count, _ = HireRequest.objects.filter(id__in=uuid_list).delete()
        self.log_action(
        user=request.user if request.user.is_authenticated else None,
        action_type="Deleted",
        model_name="HireRequest",
        description=f"Successfully deleted {count} HireRequests for IDs: {uuid_list}"
    )
        
        # Return the count of deleted objects
        return Response({"deleted": count}, status=status.HTTP_204_NO_CONTENT)
    
class HireRequestListCreateView(ActionLoggingMixin,generics.ListCreateAPIView):
    queryset = HireRequest.objects.all()
    serializer_class = HireRequestSerializer
    permission_classes = [AllowAny] 
    
    def get(self, request, *args, **kwargs):
        # Log the action  
        user = request.user if request.user.is_authenticated else None
        self.log_action(
            user=user,
            action_type="Listed",
            model_name="HireRequest"
        )
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
    
        # Log the action
        user = request.user if request.user.is_authenticated else None
        self.log_action(
            user=user,
            action_type="Created",
            model_name="Housekeeper"
        )
        
        test_mode = request.data.get('test_mode', False)
        # Retrieve request details
        request_details = {
            'housekeeper': serializer.validated_data.get('housekeeper'),
            'requester_contact': serializer.validated_data.get('requester_contact'),
            'request_date': serializer.validated_data.get('request_date'),
            'duration': serializer.validated_data.get('duration'),
            'pericepernationality_id': serializer.validated_data.get('pericepernationality_id.price'),
            'total_price': serializer.validated_data.get('total_price'),
            'status': serializer.validated_data.get('status'),
        }
        
        # Send notification to the requester with request details
        phone_number = serializer.validated_data.get('requester_contact')
        send_message(phone_number, request_details,test_mode=test_mode)
        print(send_message)
        
        success, message = send_message(phone_number, request_details, test_mode=test_mode)
    
        return Response({
        'message': message
    }, status=status.HTTP_201_CREATED if success else status.HTTP_500_INTERNAL_SERVER_ERROR, headers=headers)

     

class HireRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HireRequest.objects.all()
    serializer_class = HireRequestSerializer
    permission_classes = [AllowAny] 
    
    
############## update hire request status ####################################
class HousekeeperBatchStatusUpdateView(ActionLoggingMixin,APIView):
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
        uuid_list = [UUID(id_str) for id_str in ids.split(',')]
        new_status_name = request.query_params.get('status', '')
        self.log_action(
        user=request.user if request.user.is_authenticated else None,
        action_type="Patch Requested",
        model_name="HireRequest",
        description=f"Patch request with IDs: {ids} and new status: {new_status_name}"
    )

        # Split the 'ids' parameter by commas and convert to integers
        try:
            # ids = list(map(int, ids.split(',')))
            uuid_list = [UUID(id_str) for id_str in ids.split(',')]
        except ValueError:
            self.log_action(
            user=request.user if request.user.is_authenticated else None,
            action_type="Error",
            model_name="HireRequest",
            description="Invalid ID format in patch request"
        )
            
            return Response({"error": "Invalid ID format. Please provide a comma-separated list of integers."}, status=status.HTTP_400_BAD_REQUEST)

        if not new_status_name:
            return Response({"error": "Status value is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the Status object based on the provided status name
        try:
            new_status = Status.objects.get(Status=new_status_name)
        except Status.DoesNotExist:
            self.log_action(
            user=request.user if request.user.is_authenticated else None,
            action_type="Error",
            model_name="HireRequest",
            description=f"Status '{new_status_name}' does not exist."
        )
            return Response({"error": f"Status '{new_status_name}' does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Query the Housekeeper objects with the given IDs
        housekeepers = HireRequest.objects.filter(id__in=uuid_list)
        if not housekeepers.exists():
            self.log_action(
            user=request.user if request.user.is_authenticated else None,
            action_type="Error",
            model_name="HireRequest",
            description="No Hire Requests found for the provided IDs."
        )
            return Response({"error": "No Hire Requests found for the provided IDs."}, status=status.HTTP_404_NOT_FOUND)

        # Update the status field for the queried Housekeeper objects
        housekeepers.update(status=new_status)
        
        self.log_action(
        user=request.user if request.user.is_authenticated else None,
        action_type="Updated",
        model_name="HireRequest",
        description=f"Successfully updated status for IDs: {ids} to {new_status_name}"
    )
                
        # Update Status and Housekeeper Availability
        for hire_request in housekeepers:
            hire_request.status = new_status
            hire_request.save() # Save to trigger the update
            

            if new_status.Status == "Approved":
                housekeeper = hire_request.housekeeper
                housekeeper.is_available = False
                housekeeper.save()
            else:
                housekeeper = hire_request.housekeeper
                housekeeper.is_available = True
                housekeeper.save()
        self.log_action(
        user=request.user if request.user.is_authenticated else None,
        action_type="Updated",
        model_name="HireRequest",
        description=f"Successfully updated status for IDs: {ids} to {new_status_name}"
    )
                
                   
        return Response({"message": "Status updated successfully."}, status=status.HTTP_200_OK)
     
        
    
    
################################################################################

class RecruitmentRequestBatchDetailView(ActionLoggingMixin,APIView):
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
            # ids = list(map(int, ids.split(',')))
            uuid_list = [UUID(id_str) for id_str in ids.split(',')]
        except ValueError:
            self.log_action(
            user=request.user if request.user.is_authenticated else None,
            action_type="Error",
            model_name="RecruitmentRequest",
            description="Invalid ID format in request"
            )
            return Response({"error": "Invalid ID format. Please provide a comma-separated list of integers."}, status=status.HTTP_400_BAD_REQUEST)

        # Query the Housekeeper objects with the given IDs
        housekeepers = RecruitmentRequest.objects.filter(id__in=uuid_list)

        # Serialize the data
        serializer = RecruitmentRequestSerializer(housekeepers, many=True)
        self.log_action(
            user=request.user if request.user.is_authenticated else None,
            action_type="Retrieved",
            model_name="RecruitmentRequest",
            description=f"Successfully retrieved {len(housekeepers)} HireRequests for IDs: {ids}"
        )
        
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
            # ids = list(map(int, ids.split(',')))
            uuid_list = [UUID(id_str) for id_str in ids.split(',')]
        except ValueError:
            self.log_action(
            user=request.user if request.user.is_authenticated else None,
            action_type="Error",
            model_name="RecruitmentRequest",
            description="Invalid ID format in request"
            )
            return Response({"error": "Invalid ID format. Please provide a comma-separated list of integers."}, status=status.HTTP_400_BAD_REQUEST)

        # Delete the Housekeeper objects with the given IDs
        count, _ = RecruitmentRequest.objects.filter(id__in=uuid_list).delete()
        self.log_action(
        user=request.user if request.user.is_authenticated else None,
        action_type="Deleted",
        model_name="RecruitmentRequest",
        description=f"Successfully deleted {count} RecruitmentRequest for IDs: {ids}"
    )

        # Return the count of deleted objects
        return Response({"deleted": count}, status=status.HTTP_204_NO_CONTENT)
    

    

class RecruitmentRequestListCreateView(ActionLoggingMixin,generics.ListCreateAPIView):
    queryset = RecruitmentRequest.objects.all()
    serializer_class = RecruitmentRequestSerializer
    permission_classes = [AllowAny] 
    
    def get(self, request, *args, **kwargs):
        # Log the action  
        user = request.user if request.user.is_authenticated else None
        self.log_action(
            user=user,
            action_type="Listed",
            model_name="RecruitmentRequest",
        )
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
    
        # Log the action
        user = request.user if request.user.is_authenticated else None
        self.log_action(
            user=user,
            action_type="Created",
            model_name="RecruitmentRequest"
        )
        
        test_mode = request.data.get('test_mode', False)
        # Retrieve request details
        request_details = {
            'housekeeper': serializer.validated_data.get('housekeeper'),
            'requester':serializer.validated_data.get('requester'),
            'requester_contact': serializer.validated_data.get('requester_contact'),
            'request_date': serializer.validated_data.get('request_date'),
            'visa_status':serializer.validated_data.get('visa_status'),
            'status': serializer.validated_data.get('status'),
        }
        
        # Send notification to the requester with request details
        phone_number = serializer.validated_data.get('requester_contact')
        send_message(phone_number, request_details,test_mode=test_mode)
        print(send_message)
        
        success, message = send_message(phone_number, request_details, test_mode=test_mode)
    
        return Response({
        'message': message
    }, status=status.HTTP_201_CREATED if success else status.HTTP_500_INTERNAL_SERVER_ERROR, headers=headers)

     


class RecruitmentRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RecruitmentRequest.objects.all()
    serializer_class = RecruitmentRequestSerializer
    permission_classes = [AllowAny] 
    
    
    ########## updating ################################
class RecruitmentBatchStatusUpdateView(ActionLoggingMixin,APIView):
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
        
        self.log_action(
        user=request.user if request.user.is_authenticated else None,
        action_type="Patch Requested",
        model_name="RecruitmentRequest",
        description=f"Patch request with IDs: {ids} and new status: {new_status_name}"
    )

        # Split the 'ids' parameter by commas and convert to integers
        try:
            # ids = list(map(int, ids.split(',')))
            uuid_list = [UUID(id_str) for id_str in ids.split(',')]
        except ValueError:
            self.log_action(
            user=request.user if request.user.is_authenticated else None,
            action_type="Error",
            model_name="RecruitmentRequest",
            description="Invalid ID format in patch request"
        )
            return Response({"error": "Invalid ID format. Please provide a comma-separated list of integers."}, status=status.HTTP_400_BAD_REQUEST)

        if not new_status_name:
            return Response({"error": "Status value is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the Status object based on the provided status name
        try:
            new_status = Status.objects.get(Status=new_status_name)
        except Status.DoesNotExist:
            self.log_action(
            user=request.user if request.user.is_authenticated else None,
            action_type="Error",
            model_name="RecruitmentRequest",
            description=f"Status '{new_status_name}' does not exist."
        )
            return Response({"error": f"Status '{new_status_name}' does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Query the Housekeeper objects with the given IDs
        Recruitment = RecruitmentRequest.objects.filter(id__in=uuid_list)

        if not Recruitment.exists():
            self.log_action(
            user=request.user if request.user.is_authenticated else None,
            action_type="Error",
            model_name="RecruitmentRequest",
            description="No Recruitment Requests found for the provided IDs."
        )
            return Response({"error": "No Recruitment Requests found for the provided IDs."}, status=status.HTTP_404_NOT_FOUND)

        # Update the status field for the queried Housekeeper objects
        Recruitment.update(status=new_status)
        
        self.log_action(
        user=request.user if request.user.is_authenticated else None,
        action_type="Updated",
        model_name="RecruitmentRequest",
        description=f"Successfully updated status for IDs: {ids} to {new_status_name}"
    )
        
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
            self.log_action(
            user=request.user if request.user.is_authenticated else None,
            action_type="Updated",
            model_name="RecruitmentRequest",
            description=f"Successfully updated status for IDs: {ids} to {new_status_name}"
    )
                
        
                   
        return Response({"message": "Status updated successfully."}, status=status.HTTP_200_OK)
        
    
    
    
    
########################################################################################################


class TransferRequestBatchDetailView(ActionLoggingMixin,APIView):
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
            # ids = list(map(int, ids.split(',')))
            uuid_list = [UUID(id_str) for id_str in ids.split(',')]
        except ValueError:
            self.log_action(
            user=request.user if request.user.is_authenticated else None,
            action_type="Error",
            model_name="TransferRequest",
            description="Invalid ID format in  request"
        )
            return Response({"error": "Invalid ID format. Please provide a comma-separated list of integers."}, status=status.HTTP_400_BAD_REQUEST)

        # Query the Housekeeper objects with the given IDs
        housekeepers = TransferRequest.objects.filter(id__in=uuid_list)

        # Serialize the data
        serializer = TransferRequestSerializer(housekeepers, many=True)
        self.log_action(
            user=request.user if request.user.is_authenticated else None,
            action_type="Retrieved",
            model_name="TransferRequest",
            description=f"Successfully retrieved {len(housekeepers)} TransferRequest for IDs: {ids}"
        )
        
        
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
            # ids = list(map(int, ids.split(',')))
            uuid_list = [UUID(id_str) for id_str in ids.split(',')]
        except ValueError:
            self.log_action(
                user=request.user if request.user.is_authenticated else None,
                action_type="Error",
                model_name="TransferRequest",
                description="Invalid ID format in request"
            )
           
            return Response({"error": "Invalid ID format. Please provide a comma-separated list of integers."}, status=status.HTTP_400_BAD_REQUEST)

        # Delete the Housekeeper objects with the given IDs
        count, _ = TransferRequest.objects.filter(id__in=uuid_list).delete()
        
        self.log_action(
        user=request.user if request.user.is_authenticated else None,
        action_type="Deleted",
        model_name="TransferRequest",
        description=f"Successfully deleted {count} TransferRequest for IDs: {ids}"
    )

        # Return the count of deleted objects
        return Response({"deleted": count}, status=status.HTTP_204_NO_CONTENT)
    
    
    
    
class TransferRequestListCreateView(ActionLoggingMixin,generics.ListCreateAPIView):
    queryset = TransferRequest.objects.all()
    serializer_class = TransferRequestSerializer
    permission_classes = [AllowAny] 
    
    def get(self, request, *args, **kwargs):
        # Log the action  
        user = request.user if request.user.is_authenticated else None
        self.log_action(
            user=user,
            action_type="Listed",
            model_name="TransferRequest"
        )
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
    
        # Log the action
        user = request.user if request.user.is_authenticated else None
        self.log_action(
            user=user,
            action_type="Created",
            model_name="TransferRequest"
        )
        
        test_mode = request.data.get('test_mode', False)
        # Retrieve request details
        request_details = {
            'housekeeper': serializer.validated_data.get('housekeeper'),
            'requester':serializer.validated_data.get('requester'),
            'requester_contact': serializer.validated_data.get('requester_contact'),
             'request_date': serializer.validated_data.get('request_date'),
            'status': serializer.validated_data.get('status'),
        }
        
        # Send notification to the requester with request details
        phone_number = serializer.validated_data.get('requester_contact')
        send_message(phone_number, request_details,test_mode=test_mode)
        print(send_message)
        
        success, message = send_message(phone_number, request_details, test_mode=test_mode)
    
        return Response({
        'message': message
    }, status=status.HTTP_201_CREATED if success else status.HTTP_500_INTERNAL_SERVER_ERROR, headers=headers)

    

class TransferRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TransferRequest.objects.all()
    serializer_class = TransferRequestSerializer
    permission_classes = [AllowAny] 
    

    
class TransferBatchStatusUpdateView(ActionLoggingMixin,APIView):
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
        
        self.log_action(
        user=request.user if request.user.is_authenticated else None,
        action_type="Patch Requested",
        model_name="TransferRequest",
        description=f"Patch request with IDs: {ids} and new status: {new_status_name}"
    )

        # Split the 'ids' parameter by commas and convert to integers
        try:
            # ids = list(map(int, ids.split(',')))
            uuid_list = [UUID(id_str) for id_str in ids.split(',')]
        except ValueError:
            self.log_action(
                user=request.user if request.user.is_authenticated else None,
                action_type="Error",
                model_name="TransferRequest",
                description="Invalid ID format in request"
            )
            return Response({"error": "Invalid ID format. Please provide a comma-separated list of integers."}, status=status.HTTP_400_BAD_REQUEST)

        if not new_status_name:
            return Response({"error": "Status value is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the Status object based on the provided status name
        try:
            new_status = Status.objects.get(Status=new_status_name)
        except Status.DoesNotExist:
            self.log_action(
            user=request.user if request.user.is_authenticated else None,
            action_type="Error",
            model_name="TransferRequest",
            description=f"Status '{new_status_name}' does not exist."
        )
            return Response({"error": f"Status '{new_status_name}' does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Query the Housekeeper objects with the given IDs
        Transfer = TransferRequest.objects.filter(id__in=uuid_list)

        if not Transfer.exists():
            self.log_action(
            user=request.user if request.user.is_authenticated else None,
            action_type="Error",
            model_name="TransferRequest",
            description="No transfer Requests found for the provided IDs."
        )
            return Response({"error": "No Transfer Requests found for the provided IDs."}, status=status.HTTP_404_NOT_FOUND)

        # Update the status field for the queried Housekeeper objects
        Transfer.update(status=new_status)
        self.log_action(
        user=request.user if request.user.is_authenticated else None,
        action_type="Updated",
        model_name="TransferRequest",
        description=f"Successfully updated status for IDs: {ids} to {new_status_name}"
    )
        
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
            self.log_action(
        user=request.user if request.user.is_authenticated else None,
        action_type="Updated",
        model_name="TransferRequest",
        description=f"Successfully updated status for IDs: {ids} to {new_status_name}"
    )
        
     
        return Response({"message": "Status updated successfully."}, status=status.HTTP_200_OK)
        
    
    
    
    

