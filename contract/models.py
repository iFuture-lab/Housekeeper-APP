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
    package_details = models.ForeignKey(CustomPackage,on_delete=models.CASCADE,null=True)
    payment_details = models.ForeignKey(Payment,on_delete=models.CASCADE,null=True)
    contract_terms = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed')],null=True,blank=True)
    request_type = models.ForeignKey(ServiceType,on_delete=models.CASCADE,null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    contract_file = models.TextField(null=True, blank=True)
    hire_request = models.ForeignKey(HireRequest, on_delete=models.CASCADE, null=True, blank=True)
    transfer_request = models.ForeignKey(TransferRequest, on_delete=models.CASCADE, null=True, blank=True)
    recruitment_request= models.ForeignKey(RecruitmentRequest, on_delete=models.CASCADE, null=True, blank=True)
    
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
        
        
    def save(self, *args, **kwargs):
        if not self.contract_number:
            with transaction.atomic():
                self.contract_number = self.generate_contract_number()
                if Contract.objects.filter(contract_number=self.contract_number).exists():
                    raise ValidationError("Generated contract number already exists.")
        super().save(*args, **kwargs)

    def generate_contract_number(self):
    # Retrieve the last contract number, ensuring that it is numeric
        last_contract = Contract.objects.order_by('-contract_number').values_list('contract_number', flat=True).first()

        if last_contract and last_contract.isdigit():
            new_number = int(last_contract) + 1
        else:
            new_number = 1

        return str(new_number).zfill(5)

    # def save(self, *args, **kwargs):
    #     if not self.contract_number:
    #         new_contract_number = self.generate_contract_number()
    #         if Contract.objects.filter(contract_number=new_contract_number).exists():
    #             raise ValidationError("Generated contract number already exists.")
    #         self.contract_number = new_contract_number
    #     super().save(*args, **kwargs)

    # def generate_contract_number(self):
    #     # Convert contract_number to integers, ignoring non-numeric values
    #     last_contract = Contract.objects.annotate(
    #         contract_num_as_int=Cast('contract_number', IntegerField())
    #     ).order_by('-contract_num_as_int').first()

    #     if not last_contract or not last_contract.contract_number.isdigit():
    #         return '00001'

    #     last_number = int(last_contract.contract_number)
    #     new_number = last_number + 1
    #     return str(new_number).zfill(5)
    
   
    
    
    


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

