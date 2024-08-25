from .models import Nationallity
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from .serializers import NationalitySerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import generics
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from uuid import UUID
from django.db import IntegrityError

class NationalityCreateView(generics.ListCreateAPIView):
    queryset = Nationallity.objects.all()
    serializer_class = NationalitySerializer
    permission_classes = [AllowAny]
    
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except IntegrityError:
            
            return Response({"Nationality": "This nationality already exists."}, status=status.HTTP_400_BAD_REQUEST)

   

class NationalityRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Nationallity.objects.all()
    serializer_class = NationalitySerializer
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        return Response({
            'id': instance.id,
            'image_url': instance.image.url
        })

    
    
    
################# Get manay & delete manay ################################

class NationalitiesBatchDetailView(APIView):
    permission_classes = [AllowAny]
    serializer_class = NationalitySerializer
     
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
            return Response({"error": "Invalid ID format. Please provide a comma-separated list of integers."}, status=status.HTTP_400_BAD_REQUEST)

        # Query the Housekeeper objects with the given IDs
        national = Nationallity.objects.filter(id__in=uuid_list)

        # Serialize the data
        serializer = NationalitySerializer(national, many=True)
        
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
        uuid_list = [UUID(id_str) for id_str in ids.split(',')]

        # Split the 'ids' parameter by commas and convert to integers
        try:
            # ids = list(map(int, ids.split(',')))
            uuid_list = [UUID(id_str) for id_str in ids.split(',')]
        except ValueError:
            return Response({"error": "Invalid ID format. Please provide a comma-separated list of integers."}, status=status.HTTP_400_BAD_REQUEST)

        # Delete the Housekeeper objects with the given IDs
        count, _ = Nationallity.objects.filter(id__in=uuid_list).delete()

        # Return the count of deleted objects
        return Response({"deleted": count}, status=status.HTTP_204_NO_CONTENT)
    