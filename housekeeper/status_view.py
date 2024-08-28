from .models import Status
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from .serializer import StatusSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import generics
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .permissions import MethodBasedPermissionsMixin

class StatusCreateView(MethodBasedPermissionsMixin,generics.ListCreateAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    # permission_classes = [AllowAny] 

class StatusDetailView(MethodBasedPermissionsMixin,generics.RetrieveUpdateDestroyAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    # permission_classes = [AllowAny] 
    
    
    
################# Get manay & delete manay ################################

class StatusBatchDetailView(MethodBasedPermissionsMixin,APIView):
    # permission_classes = [AllowAny]
    serializer_class = StatusSerializer
     
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
            ids = list(map(int, ids.split(',')))
        except ValueError:
            return Response({"error": "Invalid ID format. Please provide a comma-separated list of integers."}, status=status.HTTP_400_BAD_REQUEST)

       
        state = Status.objects.filter(id__in=ids)

        serializer = StatusSerializer(state, many=True)
        
      
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
        except ValueError:
            return Response({"error": "Invalid ID format. Please provide a comma-separated list of integers."}, status=status.HTTP_400_BAD_REQUEST)

        
        count, _ =Status.objects.filter(id__in=ids).delete()


        return Response({"deleted": count}, status=status.HTTP_204_NO_CONTENT)
    