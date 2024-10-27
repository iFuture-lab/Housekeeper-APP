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
from housekeeper.permissions import MethodBasedPermissionsMixin

class NationalityCreateView(MethodBasedPermissionsMixin,generics.ListCreateAPIView):
    queryset = Nationallity.objects.all()
    serializer_class = NationalitySerializer
    permission_classes = [AllowAny]
    
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.data.get('Nationality') and Nationallity.objects.filter(Nationality=request.data.get('Nationality')).exists():
            return Response({"Nationality": "This nationality already exists."}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class NationalityRequestDetailView(MethodBasedPermissionsMixin,generics.RetrieveUpdateDestroyAPIView):
    queryset = Nationallity.objects.all()
    serializer_class = NationalitySerializer
    permission_classes = [AllowAny]

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        nat = Nationallity.objects.filter(id=self.get_object().id)
        print(request.data.keys().__contains__('image'))
        if request.data.get('Nationality'):
            # print(self.get_object().id)
            # nat = Nationallity.objects.filter(Nationality=request.data.get('Nationality'))
            if nat.exists() and nat.first().id != self.get_object().id:
                return Response({"Nationality": "This nationality already exists."}, status=status.HTTP_400_BAD_REQUEST)
        if request.data.keys().__contains__('image'):
            print('here')
            if request.data.get('image') is None:
                nat.first().image.delete()
                nat.first().save()
        serializer.save()
        return super().patch(request, *args, **kwargs)
    
    # def get(self, request, *args, **kwargs):
        # instance = self.get_object()
        # return Response({
        #     'id': instance.id,
        #     'image_url': instance.image.url
        # })

    
    
    
################# Get manay & delete manay ################################

class NationalitiesBatchDetailView(MethodBasedPermissionsMixin,APIView):
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
        
        ids = request.query_params.get('ids', '')

      
        try:
            # ids = list(map(int, ids.split(',')))
            if ids.endswith(','):
                ids = ids.split(',')[:-1]
            else:
                ids = ids.split(',')
            uuid_list = [UUID(id_str) for id_str in ids]
        except ValueError:
            return Response({"error": "Invalid ID format. Please provide a comma-separated list of UUIDs."}, status=status.HTTP_400_BAD_REQUEST)

  
        national = Nationallity.objects.filter(id__in=uuid_list)

       
        serializer = NationalitySerializer(national, many=True)
   
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
            if ids.endswith(','):
                ids = ids.split(',')[:-1]
            else:
                ids = ids.split(',')
            uuid_list = [UUID(id_str) for id_str in ids]
        except ValueError:
            return Response({"error": "Invalid ID format. Please provide a comma-separated list of UUIDs."}, status=status.HTTP_400_BAD_REQUEST)

        
        count, _ = Nationallity.objects.filter(id__in=uuid_list).delete()

        # Return the count of deleted objects
        return Response({"deleted": count}, status=status.HTTP_204_NO_CONTENT)
    