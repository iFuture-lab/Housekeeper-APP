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
from rest_framework.views import APIView
from .models import TempoararyDiscount
from uuid import UUID

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
    

class PackageBatchView(APIView):
    permission_classes = [AllowAny]
    serializer_class = CustomPackageSerializer
     
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

        # Split the 'ids' parameter by commas and convert to UUIDs
        try:
            # ids = list(map(int, ids.split(',')))
            # uuid_list = [UUID(id_str) for id_str in ids.split(',')]
            if ids.endswith(','):
                ids = ids.split(',')[:-1]
            else:
                ids = ids.split(',')
            uuid_list = [UUID(id_str) for id_str in ids]
        except ValueError:
            return Response({"error": "Invalid ID format. Please provide a comma-separated list of UUIDs."}, status=status.HTTP_400_BAD_REQUEST)

        # Query the Housekeeper objects with the given IDs
        employee= CustomPackage.objects.filter(id__in=uuid_list)

        # Serialize the data
        serializer = CustomPackageSerializer(employee, many=True)
        
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

        # Split the 'ids' parameter by commas and convert to UUIDs
        try:
            # ids = list(map(int, ids.split(',')))
            if ids.endswith(','):
                ids = ids.split(',')[:-1]
            else:
                ids = ids.split(',')
            uuid_list = [UUID(id_str) for id_str in ids]
        except ValueError:
            return Response({"error": "Invalid ID format. Please provide a comma-separated list of UUIDs."}, status=status.HTTP_400_BAD_REQUEST)

        # Delete the Housekeeper objects with the given IDs
        count, _ = CustomPackage.objects.filter(id__in=uuid_list).delete()

        # Return the count of deleted objects
        return Response({"deleted": count}, status=status.HTTP_204_NO_CONTENT)

class DiscountRetrieveUpdateDestroyView(MethodBasedPermissionsMixin,generics.RetrieveUpdateDestroyAPIView):
    queryset = TempoararyDiscount.objects.all()
    serializer_class = DiscountSerializer
    # permission_classes = [AllowAny]
   
    
    
class DiscountCreateView(MethodBasedPermissionsMixin,generics.ListCreateAPIView):
    queryset = TempoararyDiscount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [AllowAny] 
    

class DiscountBatchView(APIView):
    permission_classes = [AllowAny]
    serializer_class = DiscountSerializer
     
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

        # Split the 'ids' parameter by commas and convert to UUIDs
        try:
            # ids = list(map(int, ids.split(',')))
            # uuid_list = [UUID(id_str) for id_str in ids.split(',')]
            if ids.endswith(','):
                ids = ids.split(',')[:-1]
            else:
                ids = ids.split(',')
            uuid_list = [UUID(id_str) for id_str in ids]
        except ValueError:
            return Response({"error": "Invalid ID format. Please provide a comma-separated list of UUIDs."}, status=status.HTTP_400_BAD_REQUEST)

        # Query the Housekeeper objects with the given IDs
        employee= TempoararyDiscount.objects.filter(id__in=uuid_list)

        # Serialize the data
        serializer = DiscountSerializer(employee, many=True)
        
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

        # Split the 'ids' parameter by commas and convert to UUIDs
        try:
            # ids = list(map(int, ids.split(',')))
            if ids.endswith(','):
                ids = ids.split(',')[:-1]
            else:
                ids = ids.split(',')
            uuid_list = [UUID(id_str) for id_str in ids]
        except ValueError:
            return Response({"error": "Invalid ID format. Please provide a comma-separated list of UUIDs."}, status=status.HTTP_400_BAD_REQUEST)

        # Delete the Housekeeper objects with the given IDs
        count, _ = TempoararyDiscount.objects.filter(id__in=uuid_list).delete()

        # Return the count of deleted objects
        return Response({"deleted": count}, status=status.HTTP_204_NO_CONTENT)

class PromotionCodeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TempoararyDiscount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [AllowAny] 
    
    
    
class PromotionCodeCreateView(generics.ListCreateAPIView):
    queryset = TempoararyDiscount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [AllowAny] 
