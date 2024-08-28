from rest_framework import serializers
from .models import Religion
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import generics
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .permissions import MethodBasedPermissionsMixin


#################serilizer#########################################
class ReligionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Religion
        fields = ['id', 'name']
        
class ReligionCreateView(MethodBasedPermissionsMixin,generics.ListCreateAPIView):
    queryset = Religion.objects.all()
    serializer_class = ReligionSerializer
    # permission_classes = [AllowAny] 

class ReligionDetailView(MethodBasedPermissionsMixin,generics.RetrieveUpdateDestroyAPIView):
    queryset = Religion.objects.all()
    serializer_class = ReligionSerializer
    # permission_classes = [AllowAny] 
    
    
    
################# Get manay & delete manay ################################

class ReligionBatchDetailView(MethodBasedPermissionsMixin,APIView):
    # permission_classes = [AllowAny]
    serializer_class = ReligionSerializer
     
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
        religion= Religion.objects.filter(id__in=ids)

        # Serialize the data
        serializer = ReligionSerializer(religion, many=True)
        
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
        count, _ =Religion.objects.filter(id__in=ids).delete()

        # Return the count of deleted objects
        return Response({"deleted": count}, status=status.HTTP_204_NO_CONTENT)
    
        
        

