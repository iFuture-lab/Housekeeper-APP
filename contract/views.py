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

class ContractCreateView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    
    def check_template_path(request):
        template_name = 'contract_Recruitment.docx'
        template_path = os.path.join(settings.BASE_DIR, 'templates', template_name)
        print(template_path)
        if os.path.exists(template_path):
            print("hhhhhhhhhhhhhhhhhhhhhhh")
            return HttpResponse(f'Template found at: {template_path}')
        else:
            print("notttttttttttttttttttttttttt")
            return HttpResponse(f'Template not found at: {template_path}')
    
 

    

    def perform_create(self, serializer):
        contract = serializer.save(status='Pending')
        encoded_contract = self.generate_contract(contract)
        contract.contract_file = encoded_contract
        contract.status = 'Completed'
        contract.save()
        
    

    def generate_contract(self, contract):
        template_name = 'contract_Recruitment.docx'
        template_path = os.path.join(settings.BASE_DIR, 'templates', template_name)
        
        print(f"Template path: {template_path}")
        print(f"File exists: {os.path.exists(template_path)}")
        
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template file not found at {template_path}")
        
        print(template_path)
        
        
        doc = Document(template_path)
        print(doc)
    
        
        for paragraph in doc.paragraphs:
            paragraph.text = paragraph.text.replace('{contract_number}', contract.contract_number)
            paragraph.text = paragraph.text.replace('{customer_id}', str(contract.customer_id.Fullname))
            paragraph.text = paragraph.text.replace('{package_details}', contract.package_details)
            paragraph.text = paragraph.text.replace('{payment_details}', contract.payment_details)
            paragraph.text = paragraph.text.replace('{contract_terms}', contract.contract_terms)
            paragraph.text = paragraph.text.replace('{start_date}', str(contract.start_date))
            paragraph.text = paragraph.text.replace('{end_date}', str(contract.end_date))
            paragraph.text = paragraph.text.replace('{status}', contract.status)
            paragraph.text = paragraph.text.replace('{request_type}', contract.request_type)

       
        buffer = io.BytesIO()
        doc.save(buffer)
        buffer.seek(0)

        encoded_file = base64.b64encode(buffer.read()).decode('utf-8')
        return encoded_file

class ContractListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer

class ContractDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [AllowAny]
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
