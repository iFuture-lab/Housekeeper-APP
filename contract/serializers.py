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

logger = logging.getLogger(__name__)

class UserInterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInterest
        fields = '__all__'

    def create(self, validated_data):
        return UserInterest.objects.create(**validated_data)
  
        
class ContractSerializer(serializers.ModelSerializer):
    
    contract_file_base64 = serializers.SerializerMethodField()
    contract_file_url = serializers.SerializerMethodField()

    class Meta:
        model = Contract
        fields = '__all__'
        read_only_fields = ('contract_file_url', 'contract_file_base64')

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
            return os.path.join(settings.MEDIA_URL, 'contracts', file_name)
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
        
    