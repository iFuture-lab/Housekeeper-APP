from django.db import models,transaction
import uuid
from login.models import CustomUser
from payment.models import Payment
from temporary_discount.models import CustomPackage
from service_type.models import ServiceType

from django.db.models.functions import Cast
from django.db.models import IntegerField,Max
from django.utils import timezone
from login.models import CustomUser
from django.core.exceptions import ValidationError
from housekeeper.models import HireRequest,TransferRequest,RecruitmentRequest,EmploymentType
from nationality.models import Nationallity
from django.core.validators import FileExtensionValidator

import base64
from django.core.files.base import ContentFile
import os
from django.conf import settings


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        #  filters out soft-deleted records
        return super().get_queryset().filter(deleted_at__isnull=True)

    def deleted(self):
        # Return only soft-deleted records
        return super().get_queryset().filter(deleted_at__isnull=False)

    def with_deleted(self):
        # all the records 
        return super().get_queryset()


class Contract(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contract_number = models.CharField(max_length=5, blank=True)
    customer_id = models.ForeignKey(CustomUser,on_delete=models.CASCADE,)
    #package_details = models.ForeignKey(CustomPackage,on_delete=models.CASCADE,null=True)
    #payment_details = models.ForeignKey(Payment,on_delete=models.CASCADE,null=True)
    #contract_terms = models.TextField()
    #start_date = models.DateField(null=True,blank=True)
    #end_date = models.DateField(null=True,blank=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed'),('Rejected', 'Rejected'),('Approved', 'Approved')],null=True,blank=True)
    request_type = models.ForeignKey(ServiceType,on_delete=models.CASCADE,null=True,blank= True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    # contract_file = models.FileField(upload_to='contracts/', null=True, blank=True)
    contract_file = models.TextField(null=True, blank=True)
    hire_request = models.ForeignKey(HireRequest, on_delete=models.CASCADE, null=True, blank=True)
    transfer_request = models.ForeignKey(TransferRequest, on_delete=models.CASCADE, null=True, blank=True)
    recruitment_request= models.ForeignKey(RecruitmentRequest, on_delete=models.CASCADE, null=True, blank=True)
    
    objects = SoftDeleteManager()  
    all_objects = models.Manager()
    
    
    def save_pdf_from_base64(self, base64_pdf_data, filename):
        """Save PDF from base64 string to the media/contracts directory."""
        try:
            if base64_pdf_data:
                if base64_pdf_data.startswith('data:application/pdf;base64,'):
                    base64_pdf_data = base64_pdf_data.split(';base64,')[1]
                    pdf_data = base64.b64decode(base64_pdf_data)
                    file_path = os.path.join(settings.MEDIA_ROOT, 'contracts', filename)
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    with open(file_path, 'wb') as file:
                        file.write(pdf_data)
                    self.contract_file = file_path
                else:
                    raise ValueError("Provided base64 string is not a PDF file")
        except Exception as e:
            print("Error:", e)
            raise ValueError(f"Error decoding base64 PDF: {e}")

   
        
        
    def get_contract_file_url(self):
        """Generate a URL for the stored PDF file."""
        if self.contract_file:
            file_name = os.path.basename(self.contract_file)
            return os.path.join('contracts', file_name)
        return None
        
    
    
    

class UserInterest(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    INTEREST_STATUS_CHOICES = [
        ('clicked', 'Clicked'),
        ('abandoned', 'Abandoned'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='interests')
    service = models.ForeignKey(ServiceType, on_delete=models.CASCADE, related_name='user_interests')
    timestamp = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=INTEREST_STATUS_CHOICES, blank=True, null=True)
    device_info = models.CharField(max_length=255, blank=True, null=True)
    session_data = models.JSONField(blank=True, null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    nationality = models.ForeignKey(Nationallity, on_delete=models.SET_NULL, null=True, blank=True)
    employment_type = models.ForeignKey(EmploymentType, on_delete=models.SET_NULL, null=True, blank=True)
    
    
    objects = SoftDeleteManager()  
    all_objects = models.Manager()  
    

    def delete(self):
       #soft deleting
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        # Restore a soft-deleted record 
        self.deleted_at = None
        self.save()

    def hard_delete(self):
        # delete the record in real 
        super().delete()

    def __str__(self):
        return f"{self.user.fullName} - {self.service.name} - {self.status}"

    class Meta:
        ordering = ['-timestamp']

