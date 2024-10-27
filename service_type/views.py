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
from housekeeper.models import HireRequest, TransferRequest, RecruitmentRequest, Status

class ServiceCreateView(MethodBasedPermissionsMixin,generics.ListCreateAPIView):
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer
    permission_classes = [AllowAny] 

class ServiceDetailView(MethodBasedPermissionsMixin,generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer
    permission_classes = [AllowAny] 

class ServiceByRequestStatus(MethodBasedPermissionsMixin,APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="List of services by request status",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.FORMAT_UUID),
                            'name': openapi.Schema(type=openapi.TYPE_STRING),
                            'count': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'approved': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'pending': openapi.Schema(type=openapi.TYPE_INTEGER),   
                            'paid': openapi.Schema(type=openapi.TYPE_INTEGER)
                        }
                    )
                )
            )
        }
    )
    def get(self, request):
        data = []
        
        if not ServiceType.objects.filter(name='استقدام').exists() or not ServiceType.objects.filter(name='التاجير').exists() or not ServiceType.objects.filter(name='نقل الخدمات').exists():
            for service in ServiceType.objects.all():
                result = {
                    'id': service.id,
                    'name': service.name,
                    "count": HireRequest.objects.filter(request_type=service, deleted_at=None).count() + TransferRequest.objects.filter(request_type=service, deleted_at=None).count() + RecruitmentRequest.objects.filter(request_type=service, deleted_at=None).count()
                }
                for status in Status.objects.all():
                    result[status.Status] = RecruitmentRequest.objects.filter(request_type=service, status=status, deleted_at=None).count() + HireRequest.objects.filter(request_type=service, status=status, deleted_at=None).count() + TransferRequest.objects.filter(request_type=service, status=status, deleted_at=None).count()
                data.append(result)
        else:
            service = ServiceType.objects.filter(name='نقل الخدمات').first()
            result = {
                'id': service.id,
                'name': service.name,
                "count": TransferRequest.objects.filter(deleted_at=None).count()
            }
            for status in Status.objects.all():
                result[status.Status] = TransferRequest.objects.filter(deleted_at=None, status=status).count()
            data.append(result)
            service = ServiceType.objects.filter(name='استقدام').first()
            result = {
                'id': service.id,
                'name': service.name,
                "count": RecruitmentRequest.objects.filter(deleted_at=None).count()
            }
            for status in Status.objects.all():
                result[status.Status] = RecruitmentRequest.objects.filter(deleted_at=None, status=status).count()
            data.append(result)
            service = ServiceType.objects.filter(name='التاجير').first()
            result = {
                'id': service.id,
                'name': service.name,
                "count": HireRequest.objects.filter(deleted_at=None).count()
            }
            for status in Status.objects.all():
                result[status.Status] = HireRequest.objects.filter(deleted_at=None, status=status).count()
            data.append(result)

        return Response(data)

class ServiceByRequest(MethodBasedPermissionsMixin,APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="List of services by requests",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.FORMAT_UUID),
                            'name': openapi.Schema(type=openapi.TYPE_STRING),
                            'count': openapi.Schema(type=openapi.TYPE_INTEGER),
                        }
                    )
                )
            )
        }
    )
    def get(self, request):
        data = []

        if not ServiceType.objects.filter(name='استقدام').exists() or not ServiceType.objects.filter(name='التاجير').exists() or not ServiceType.objects.filter(name='نقل الخدمات').exists():
            for service in ServiceType.objects.all():
                data.append({
                    'id': service.id,
                    'name': service.name,
                    "count": HireRequest.objects.filter(request_type=service, deleted_at=None).count() + TransferRequest.objects.filter(request_type=service, deleted_at=None).count() + RecruitmentRequest.objects.filter(request_type=service, deleted_at=None).count()
                })
        else:
            service = ServiceType.objects.filter(name='نقل الخدمات').first()
            result = {
                'id': service.id,
                'name': service.name,
                "count": TransferRequest.objects.filter(deleted_at=None).count()
            }
            data.append(result)
            service = ServiceType.objects.filter(name='استقدام').first()
            result = {
                'id': service.id,
                'name': service.name,
                "count": RecruitmentRequest.objects.filter(deleted_at=None).count()
            }
            data.append(result)
            service = ServiceType.objects.filter(name='التاجير').first()
            result = {
                'id': service.id,
                'name': service.name,
                "count": HireRequest.objects.filter(deleted_at=None).count()
            }
            data.append(result)
        return Response(data)

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
            return Response({"error": "Invalid ID format. Please provide a comma-separated list of UUIDs."}, status=status.HTTP_400_BAD_REQUEST)

     
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
            return Response({"error": "Invalid ID format. Please provide a comma-separated list of UUIDs."}, status=status.HTTP_400_BAD_REQUEST)

       
        count, _ = ServiceType.objects.filter(id__in=uuid_list).delete()

      
        return Response({"deleted": count}, status=status.HTTP_204_NO_CONTENT)
    