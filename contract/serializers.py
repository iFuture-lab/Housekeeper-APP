from rest_framework import serializers
from .models import Contract

import base64
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
import uuid

from .models import UserInterest

import logging

logger = logging.getLogger(__name__)

class UserInterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInterest
        fields = '__all__'

    def create(self, validated_data):
        return UserInterest.objects.create(**validated_data)
  
        

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'
        read_only_fields = ('contract_number',)
        
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('deleted_at', None)
        return representation

    def create(self, validated_data):
        # Get the Base64 data from the request context
        pdf_data = self.context['request'].data.get('contract_file')
        logger.debug(f'PDF Data: {pdf_data}')
        if isinstance(pdf_data, str) and 'base64,' in pdf_data:
            # Handle Base64 string
            format, pdfstr = pdf_data.split(';base64,')
            ext = format.split('/')[-1]  # Extract the file extension
            if ext != 'pdf':
                raise serializers.ValidationError("The file must be a PDF.")
            data = ContentFile(base64.b64decode(pdfstr), name=f'{uuid.uuid4()}.{ext}')
            validated_data['contract_file'] = data
        elif isinstance(pdf_data, ContentFile) or isinstance(pdf_data, InMemoryUploadedFile):
            # Handle standard file upload
            pass

        return super().create(validated_data)
        
        