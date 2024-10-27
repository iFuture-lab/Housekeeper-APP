from rest_framework import serializers
from .models import EmploymentType
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
from uuid import UUID


#################serilizer#########################################
class EmploymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmploymentType
        fields = ['id', 'name']
        
class EmploymentTypeCreateView(MethodBasedPermissionsMixin,generics.ListCreateAPIView):
    queryset = EmploymentType.objects.all()
    serializer_class = EmploymentTypeSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class EmploymentTypeDetailView(MethodBasedPermissionsMixin,generics.RetrieveUpdateDestroyAPIView):
    queryset = EmploymentType.objects.all()
    serializer_class = EmploymentTypeSerializer
    permission_classes = [AllowAny] 

################# Get manay & delete manay ################################

class EmploymentTypeBatchDetailView(APIView):
    permission_classes = [AllowAny]
    serializer_class = EmploymentTypeSerializer
     
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
        employee= EmploymentType.objects.filter(id__in=uuid_list)

        # Serialize the data
        serializer = EmploymentTypeSerializer(employee, many=True)
        
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
        count, _ =EmploymentType.objects.filter(id__in=uuid_list).delete()

        # Return the count of deleted objects
        return Response({"deleted": count}, status=status.HTTP_204_NO_CONTENT)
    
        
        

