from .models import ServiceType
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from .serializers import ServiceTypeSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import generics
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from housekeeper.permissions import MethodBasedPermissionsMixin
from uuid import UUID

class ServiceCreateView(MethodBasedPermissionsMixin,generics.ListCreateAPIView):
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer
    permission_classes = [AllowAny] 

class ServiceDetailView(MethodBasedPermissionsMixin,generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer
    permission_classes = [AllowAny] 
    
    
    
################# Get manay & delete manay ################################

class ServiceBatchDetailView(MethodBasedPermissionsMixin,APIView):
    permission_classes = [AllowAny]
    serializer_class = ServiceTypeSerializer
     
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
       
        ids = request.query_params.get('ids', '')

      
        try:
            # ids = list(map(int, ids.split(',')))
            uuid_list = [UUID(id_str) for id_str in ids.split(',')]
        except ValueError:
            return Response({"error": "Invalid ID format. Please provide a comma-separated list of integers."}, status=status.HTTP_400_BAD_REQUEST)

     
        service = ServiceType.objects.filter(id__in=uuid_list)

       
        serializer = ServiceTypeSerializer(service, many=True)
        
   
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
 
        ids = request.query_params.get('ids', '')

        try:
            ids = list(map(int, ids.split(',')))
            uuid_list = [UUID(id_str) for id_str in ids.split(',')]
        except ValueError:
            return Response({"error": "Invalid ID format. Please provide a comma-separated list of integers."}, status=status.HTTP_400_BAD_REQUEST)

       
        count, _ = ServiceType.objects.filter(id__in=uuid_list).delete()

      
        return Response({"deleted": count}, status=status.HTTP_204_NO_CONTENT)
    