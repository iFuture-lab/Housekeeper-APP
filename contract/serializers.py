from rest_framework import serializers
from .models import Contract

import base64
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
import uuid
from rest_framework.exceptions import ValidationError 

from .models import UserInterest
import os
from django.conf import settings

import logging
from temporary_discount.serializers import CustomPackageSerializer
from service_type.serializers import ServiceTypeSerializer
from service_type.models import ServiceType
from housekeeper.serializer import HousekeeperSerializer, HireRequestSerializer, RecruitmentRequestSerializer, TransferRequestSerializer, EmploymentTypeSerializer

logger = logging.getLogger(__name__)

class UserInterestSerializer(serializers.ModelSerializer):
    housekeeper_detail = HousekeeperSerializer(source='housekeeper', read_only=True)
    employment_type_detail = EmploymentTypeSerializer(source='employment_type', read_only=True)
    service_detail = ServiceTypeSerializer(source='service', read_only=True)
    custom_package_detail = CustomPackageSerializer(source='custom_package', read_only=True)
    class Meta:
        model = UserInterest
        fields = '__all__'

class UserInterestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInterest
        fields = '__all__'

    def create(self, validated_data):
        return UserInterest.objects.create(**validated_data)
  
        
class ContractSerializer(serializers.ModelSerializer):
    
    # contract_file_base64 = serializers.SerializerMethodField()
    contract_file_url = serializers.SerializerMethodField()
    request_type_detail = serializers.SerializerMethodField()
    request_type_name = serializers.SerializerMethodField()
    # request_type_detail = ServiceTypeSerializer(source='request_type', read_only=True)
    housekeeper_name = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()

    class Meta:
        model = Contract
        fields = '__all__'
        read_only_fields = ('contract_file_url', 'request_type_detail')

    def get_request_type_detail(self, obj):
        if obj.hire_request:
            return ServiceTypeSerializer(ServiceType.objects.get(id=HireRequestSerializer(obj.hire_request).data['request_type'])).data
        elif obj.transfer_request:
            return ServiceTypeSerializer(ServiceType.objects.get(id=TransferRequestSerializer(obj.transfer_request).data['request_type'])).data
        elif obj.recruitment_request:
            return ServiceTypeSerializer(ServiceType.objects.get(id=RecruitmentRequestSerializer(obj.recruitment_request).data['request_type'])).data
        else:
            return None
    
    def get_request_type_name(self, obj):
        if obj.hire_request:
            return ServiceTypeSerializer(ServiceType.objects.get(id=HireRequestSerializer(obj.hire_request).data['request_type'])).data['name']
        elif obj.transfer_request:
            return ServiceTypeSerializer(ServiceType.objects.get(id=TransferRequestSerializer(obj.transfer_request).data['request_type'])).data['name']
        elif obj.recruitment_request:
            return ServiceTypeSerializer(ServiceType.objects.get(id=RecruitmentRequestSerializer(obj.recruitment_request).data['request_type'])).data['name']
        else:
            return None

    def get_housekeeper_name(self, obj):
        if obj.hire_request:
            return HousekeeperSerializer(obj.hire_request.housekeeper).data['Name']
        elif obj.transfer_request:
            return HousekeeperSerializer(obj.transfer_request.housekeeper).data['Name']
        elif obj.recruitment_request:
            return HousekeeperSerializer(obj.recruitment_request.housekeeper).data['Name']
        else:
            return None
    
    def get_gender(self, obj):
        if obj.hire_request:
            return HousekeeperSerializer(obj.hire_request.housekeeper).data['gender']
        elif obj.transfer_request:
            return HousekeeperSerializer(obj.transfer_request.housekeeper).data['gender']
        elif obj.recruitment_request:
            return HousekeeperSerializer(obj.recruitment_request.housekeeper).data['gender']
        else:
            return None

    def get_contract_file_base64(self, obj):
        """Return the base64-encoded contract file."""
        if obj.contract_file and os.path.exists(obj.contract_file):
            with open(obj.contract_file, 'rb') as file:
                base64_pdf = base64.b64encode(file.read()).decode('utf-8')
                return f"data:application/pdf;base64,{base64_pdf}"
        return None

    def get_contract_file_url(self, obj):
        """Retrieve the URL for the contract file."""
        if obj.contract_file:
            file_name = os.path.basename(obj.contract_file)
            return f"https://ofaq.ifuture.sa{os.path.join(settings.MEDIA_URL, 'contracts', file_name)}"
        return None

    def create(self, validated_data):
        """Handle creating a contract and decoding base64 PDF."""
        base64_pdf = validated_data.pop('contract_file', None)
        contract = Contract.objects.create(**validated_data)

        if base64_pdf:
            customer_name = validated_data.get('customer_id', None)
            customer_name = customer_name.fullName if customer_name else 'Unknown'
            filename = f'{customer_name}_{contract.id}.pdf'
            contract.save_pdf_from_base64(base64_pdf, filename)

        contract.save()
        return contract      
        
    