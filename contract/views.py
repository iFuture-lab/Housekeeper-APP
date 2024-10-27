from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .models import Contract
from .serializers import ContractSerializer
from docx import Document
import base64
import io
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
import os
from django.conf import settings
from docx import Document
from django.conf import settings
from django.http import HttpResponse
import os
from .models import UserInterest
from .serializers import UserInterestSerializer, UserInterestCreateSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from rest_framework import status
from housekeeper.models import HireRequest,TransferRequest,RecruitmentRequest,Status
from service_type.models import ServiceType
from housekeeper.permissions import RolePermission,MethodBasedPermissionsMixin
import uuid
from rest_framework.permissions import AllowAny
from login.models import CustomUser
from housekeeper.serializer import CustomUserSerializer, EmploymentTypeSerializer, HousekeeperSerializer
from housekeeper.models import Housekeeper, EmploymentType
from service_type.serializers import ServiceTypeSerializer
from temporary_discount.serializers import CustomPackageSerializer
from temporary_discount.models import CustomPackage
from nationality.serializers import NationalitySerializer
from nationality.models import Nationallity

class UserInterestCreateView(MethodBasedPermissionsMixin,generics.CreateAPIView):
    queryset = UserInterest.objects.all()
    serializer_class = UserInterestCreateSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={
            201: openapi.Response(
                description="Interest created successfully.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            )
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Interest created successfully."}, status=status.HTTP_201_CREATED)

class UserInterestListView(generics.ListAPIView):
    queryset = UserInterest.objects.all()
    serializer_class = UserInterestSerializer
    
    def get_queryset(self):
        # if isinstance(self.request.user, User):
        #     return UserInterest.objects.all()
        return UserInterest.objects.filter(user=self.request.user)
    
    
class UserInterestReportView(MethodBasedPermissionsMixin, generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserInterestSerializer
    queryset = UserInterest.objects.all()

class UserInterestByCustomer(MethodBasedPermissionsMixin, APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="List of user interest by customer",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'user_id': openapi.Schema(type=openapi.FORMAT_UUID),
                            'user_detail': openapi.Schema(type=openapi.TYPE_OBJECT),
                            'services': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(
                                type=openapi.FORMAT_UUID
                            )),
                            'services_details': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(
                                openapi.TYPE_OBJECT
                            )),
                            'nationalities': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(
                                openapi.FORMAT_UUID
                            )),
                            'nationalities_details': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(
                                openapi.TYPE_OBJECT
                            )),
                            'housekeepers': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(
                                openapi.FORMAT_UUID
                            )),
                            'housekeepers_details': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(
                                openapi.TYPE_OBJECT
                            )),
                            'employment_types': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(
                                openapi.FORMAT_UUID
                            )),
                            'employment_types_details': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(
                                openapi.TYPE_OBJECT
                            )),
                            'custom_packages': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(
                                openapi.FORMAT_UUID
                            )),
                            'custom_packages_details': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(
                                openapi.TYPE_OBJECT
                            )),
                            'devices': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(
                                openapi.TYPE_STRING
                            ))
                        }
                    )
                )
            )
        }
    )
    def get(self, request):
        data = []
        for user in CustomUser.objects.all():
            interest = UserInterest.objects.filter(user=user)
            data.append({
                'user_id': user.id,
                "user_detail": CustomUserSerializer(user).data,
                "services": interest.values_list('service', flat=True).filter(service__isnull=False).distinct().order_by('service'),
                "services_details": ServiceTypeSerializer(ServiceType.objects.filter(id__in=interest.values_list('service', flat=True).filter(service__isnull=False)), many=True).data,
                "nationalities": interest.values_list('nationality', flat=True).filter(nationality__isnull=False).distinct().order_by('nationality'),
                "nationalities_details": NationalitySerializer(Nationallity.objects.filter(id__in=interest.values_list('nationality', flat=True).filter(nationality__isnull=False)), many=True).data,
                "housekeepers": interest.values_list('housekeeper', flat=True).filter(housekeeper__isnull=False).distinct().order_by('housekeeper'),
                "housekeepers_details": HousekeeperSerializer(Housekeeper.objects.filter(id__in=interest.values_list('housekeeper', flat=True).filter(housekeeper__isnull=False)), many=True).data,
                "employment_types": interest.values_list('employment_type', flat=True).filter(employment_type__isnull=False).distinct().order_by('employment_type'),
                "employment_types_details": EmploymentTypeSerializer(EmploymentType.objects.filter(id__in=interest.values_list('employment_type', flat=True).filter(employment_type__isnull=False)), many=True).data,
                "custom_packages": interest.values_list('custom_package', flat=True).filter(custom_package__isnull=False).distinct().order_by('custom_package'),
                "custom_packages_details": CustomPackageSerializer(CustomPackage.objects.filter(id__in=interest.values_list('custom_package', flat=True).filter(housekeeper__isnull=True)), many=True).data,
                "devices": interest.values_list('device_info', flat=True).filter(device_info__isnull=False).distinct().order_by('device_info'),
            })
        return Response(data)
        # if customer_id is None:
        #     data = UserInterest.objects.values('user').annotate(interests=UserInterest.objects.filter)
        #     return Response(data)
        # try:
        #     customer_uuid = uuid.UUID(customer_id)
        # except ValueError:
        #     return Response({'error': 'Invalid UUID format'}, status=status.HTTP_400_BAD_REQUEST)

        # print(f"Searching for user_interests with customer_id: {customer_uuid}")
        # queryset = UserInterest.objects.filter(customer_id=customer_uuid)
        # print(f"Found user_interests: {queryset}")
        # serializer = UserInterestSerializer(queryset, many=True)
        # return Response(serializer.data)

####################contract#####################################

class ContractsByRequester(MethodBasedPermissionsMixin, APIView):
    serializer_class = ContractSerializer
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        responses={
            200: openapi.Response('Success', ContractSerializer(many=True)),
            400: 'Bad Request',
        },
        operation_description="Get contracts by customer_id",
        manual_parameters=[
            openapi.Parameter('customer_id', openapi.IN_QUERY, description='Customer ID', type=openapi.TYPE_STRING),
        ]
    )
    def get(self, request):
        # Get the customer_id from the query parameters
        customer_id = self.request.query_params.get('customer_id', None)
        
        if customer_id is None:
            return Response({'error': 'customer_id query parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Convert the customer_id to a UUID object
            customer_uuid = uuid.UUID(customer_id)
        except ValueError:
            return Response({'error': 'Invalid UUID format'}, status=status.HTTP_400_BAD_REQUEST)

        print(f"Searching for contracts with customer_id: {customer_uuid}")
        queryset = Contract.objects.filter(customer_id=customer_uuid)
        print(f"Found contracts: {queryset}")

        serializer = self.serializer_class(queryset, many=True)
    
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    

class ContractCreateView(MethodBasedPermissionsMixin,generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    
    @swagger_auto_schema(
        request_body=ContractSerializer,
        responses= {
            201: openapi.Response(
                description="Contract created",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "success": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        "id": openapi.Schema(type=openapi.TYPE_STRING),
                        "contract_file_url": openapi.Schema(type=openapi.TYPE_STRING),
                        # "contract_file_base64": openapi.Schema(type=openapi.FORMAT_BASE64),
                    }
                )
            ),
            400: 'Bad Request',
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = ContractSerializer(data=request.data)
        count = Contract.objects.count()
        if serializer.is_valid():
            serializer.validated_data['contract_number'] = f"{count + 1:04d}"
            print(serializer.validated_data)
            contract = serializer.save()
            return Response({
                "success": True,
                "id": contract.id,
                "contract_file_url": serializer.data.get('contract_file_url'),
                # "contract_file_base64": serializer.data.get('contract_file_base64')
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @swagger_auto_schema(
        responses={
            200: openapi.Response('Success', ContractSerializer(many=True)),
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
      
    # def perform_create(self, serializer):
    #     contract = serializer.save(status='Pending')
    #     request_type = contract.request_type
    #     print("'''''''''''''''''",request_type)
    #     print("Request Type Attributes:", dir(request_type))
    
    
    #     request_type_name = getattr(request_type, 'name', None)
    #     print("Request Type Name:", request_type_name)
    #     if request_type:
    #         print("""""""""""""""""","hi")
    #     x= ServiceType.objects.get(name='Hire')
    #     y= ServiceType.objects.get(name='Transfer')
    #     z= ServiceType.objects.get(name='Recruitment')
        
    #     if request_type == x:
    #         print("I got ittttttttttttttttttt")  
    #         valid_payment = self.check_hire_request_status(contract)
    #         print("found hire request paid",valid_payment)
    #     elif request_type == y:
    #         valid_payment = self.check_transfer_request_status(contract)
    #     elif request_type == z:
    #         valid_payment = self.check_recruitment_request_status(contract)
    #     else:
    #         valid_payment = False
            
    #     if valid_payment:
    #         try:
    #             # encoded_contract = self.generate_contract(contract)
    #             # contract.contract_file = encoded_contract
    #             # contract.status = 'Completed'
    #             # contract.save()
                
                
    #             contract.status = 'Completed'
    #             contract.save(update_fields=['status'])
            
            
    #             encoded_contract = self.generate_contract(contract)
    #             contract.contract_file = encoded_contract
    #             contract.save(update_fields=['contract_file'])
    #             return Response({
    #                 'contract_number': contract.contract_number,
    #                 'contract_file': encoded_contract
    #             }, status=status.HTTP_201_CREATED)

    #         except Exception as e:
    #             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    #     else:
           
    #         contract.delete()
    #         return Response({'error': 'Payment status is not valid.'}, status=status.HTTP_400_BAD_REQUEST)


      

    # def check_hire_request_status(self, contract):
    #     if contract.hire_request:
    #         hire_request = HireRequest.objects.filter(
    #             id=contract.hire_request.id).first()
    #         status= Status.objects.get(Status='Paid')
    #         if hire_request.status== status:
    #             print("''''''''''''","I found itttttttttttt")
    #             return hire_request
    #     return False

    
    # def check_transfer_request_status(self, contract):
    #     if contract.transfer_request:
    #         transfer_request = TransferRequest.objects.filter(
    #             id=contract.transfer_request.id
    #         ).first()
    #         status= Status.objects.get(Status='Paid')
    #         if transfer_request.status== status:
    #             print("''''''''''''","I found itttttttttttt")
    #         return transfer_request
    #     return False
    
    
    # def check_recruitment_request_status(self, contract):
    #     if contract.recruitment_request:
    #         recruitment_request = RecruitmentRequest.objects.filter(
    #             id=contract.recruitment_request.id
    #         ).first()
    #         status= Status.objects.get(Status='Paid')
    #         if recruitment_request.status== status:
    #             print("''''''''''''","I found itttttttttttt")
    #         return recruitment_request
    #     return False
    
        
        
         
    # def check_template_path(request):
    #     template_name = 'contract_Recruitment.docx'
    #     template_path = os.path.join(settings.BASE_DIR, 'templates', template_name)
    #     print(template_path)
    #     if os.path.exists(template_path):
    #         print("hhhhhhhhhhhhhhhhhhhhhhh")
    #         return HttpResponse(f'Template found at: {template_path}')
    #     else:
    #         print("notttttttttttttttttttttttttt")
    #         return HttpResponse(f'Template not found at: {template_path}')
        
        
    # def generate_contract(self, contract):
    #     template_name = 'contract_Recruitment.docx'
    #     template_path = os.path.join(settings.BASE_DIR, 'templates', template_name)
    #     save_path = 'contract.docx'

    #     if not os.path.exists(template_path):
    #         raise FileNotFoundError(f"Template file not found at {template_path}")

 
    #     replacements = {
    #         '{contract_number}': str(contract.contract_number) if contract.contract_number else '',
    #         '{customer_id}': str(contract.customer_id.fullName) if contract.customer_id else '',
    #         '{package_details}': str(contract.package_details) if contract.package_details else '',
    #         '{payment_details}': str(contract.payment_details.order_id) if contract.payment_details else '',
    #         '{contract_terms}': str(contract.contract_terms) if contract.contract_terms else '',
    #         '{start_date}': contract.start_date.strftime('%Y/%m/%d') if contract.start_date else '',
    #         '{end_date}': contract.end_date.strftime('%Y/%m/%d') if contract.end_date else '',
    #         '{status}': contract.status if contract.status else '',
    #         '{request_type}': str(contract.request_type) if contract.request_type else '',
    #     }

    #     def replace_placeholders(doc, replacements):
    #         for paragraph in doc.paragraphs:
               
    #             original_text = paragraph.text
    #             print(f"Original text in paragraph: '{original_text}'")
        
           
    #             for key, value in replacements.items():
    #                 if key in paragraph.text:
    #                     paragraph.text = paragraph.text.replace(key, value)
    #                     print(f"Replaced '{key}' with '{value}'")
    #             updated_text = paragraph.text
    #             if original_text != updated_text:
    #                 print(f"Updated text in paragraph: '{updated_text}'")
    #         return doc


    #     doc = Document(template_path)
    #     print(f"Document loaded from {template_path}")

    #     doc = replace_placeholders(doc, replacements)
          
    #     buffer = io.BytesIO()
    #     doc.save(buffer)
    #     buffer.seek(0)
    #     doc.save(save_path)

    #     encoded_file = base64.b64encode(buffer.read()).decode('utf-8')
    #     return encoded_file
        

        
        # print(f"Document saved successfully to {os.path.abspath(save_path)}")
        


class ContractListView(MethodBasedPermissionsMixin,generics.ListAPIView):
    # permission_classes = [AllowAny]
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    
class ContractBatchView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ContractSerializer
     
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
            uuid_list = [uuid.UUID(id_str) for id_str in ids]
        except ValueError:
            return Response({"error": "Invalid ID format. Please provide a comma-separated list of UUIDs."}, status=status.HTTP_400_BAD_REQUEST)

        # Query the Housekeeper objects with the given IDs
        employee= Contract.objects.filter(id__in=uuid_list)

        # Serialize the data
        serializer = ContractSerializer(employee, many=True)
        
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
            uuid_list = [uuid.UUID(id_str) for id_str in ids]
        except ValueError:
            return Response({"error": "Invalid ID format. Please provide a comma-separated list of UUIDs."}, status=status.HTTP_400_BAD_REQUEST)

        # Delete the Housekeeper objects with the given IDs
        count, _ = Contract.objects.filter(id__in=uuid_list).delete()

        # Return the count of deleted objects
        return Response({"deleted": count}, status=status.HTTP_204_NO_CONTENT)

class ContractDetailView(MethodBasedPermissionsMixin,generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [AllowAny]
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
 # Save the updated document
    
        # buffer = io.BytesIO()
        # doc.save(buffer)
        # buffer.seek(0)

        # encoded_file = base64.b64encode(buffer.read()).decode('utf-8')
        # return encoded_file
        # doc.save()
        # print(f"Document saved successfully to {os.path.abspath(save_path)}")
        
        
        
        
        
        
                  
    
    

 

    

    # def perform_create(self, serializer):
    #     contract = serializer.save(status='Pending')
    #     encoded_contract = self.generate_contract(contract)
    #     contract.contract_file = encoded_contract
    #     contract.status = 'Completed'
    #     contract.save()
        
    

    # def generate_contract(self, contract):
    #     template_name = 'contract_Recruitment.docx'
    #     template_path = os.path.join(settings.BASE_DIR, 'templates', template_name)
        
    #     print(f"Template path: {template_path}")
    #     print(f"File exists: {os.path.exists(template_path)}")
        
    #     if not os.path.exists(template_path):
    #         raise FileNotFoundError(f"Template file not found at {template_path}")
        
    #     print(template_path)
        
        
    #     doc = Document(template_path)
    #     print(doc)
    
        
        # for paragraph in doc.paragraphs:
        #      paragraph.text = paragraph.text.replace('{hi}', contract.contract_number)
            # paragraph.text = paragraph.text.replace('{customer_id}', str(contract.customer_id.Fullname))
            # paragraph.text = paragraph.text.replace('{package_details}', contract.package_details)
            # paragraph.text = paragraph.text.replace('{payment_details}', contract.payment_details)
            # paragraph.text = paragraph.text.replace('{contract_terms}', contract.contract_terms)
            # paragraph.text = paragraph.text.replace('{start_date}', str(contract.start_date))
            # paragraph.text = paragraph.text.replace('{end_date}', str(contract.end_date))
            # paragraph.text = paragraph.text.replace('{status}', contract.status)
            # paragraph.text = paragraph.text.replace('{request_type}', contract.request_type)

       
        # buffer = io.BytesIO()
        # doc.save(buffer)
        # buffer.seek(0)

        # encoded_file = base64.b64encode(buffer.read()).decode('utf-8')
        # return encoded_file
        
        
        # contract = serializer.save(status='Pending')

        # # Generate and encode the contract
        # try:
        #     encoded_contract = self.generate_contract(contract)
        #     contract.contract_file = encoded_contract
        #     contract.status = 'Completed'
        #     contract.save()
        #     return Response({
        #     'contract_number': contract.contract_number,
        #     'contract_file': encoded_contract
        # }, status=status.HTTP_201_CREATED)
            
        # except Exception as e:
        #     # Handle errors gracefully and provide feedback
        #     return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
