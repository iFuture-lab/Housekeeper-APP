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
    customer_id = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    package_details = models.ForeignKey(CustomPackage,on_delete=models.CASCADE,null=True)
    payment_details = models.ForeignKey(Payment,on_delete=models.CASCADE,null=True)
    contract_terms = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed')])
    request_type = models.ForeignKey(ServiceType,on_delete=models.CASCADE,null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    contract_file = models.TextField(null=True, blank=True)
    
    objects = SoftDeleteManager()  # Custom manager
    all_objects = models.Manager()  # Default manager to access all records, including deleted

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
    
   
    
    
    
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class UserInterest(models.Model):
    INTEREST_STATUS_CHOICES = [
        ('clicked', 'Clicked'),
        ('abandoned', 'Abandoned'),
    ]

    interest_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='interests')
    service_id = models.IntegerField() # what do you mean by this like hire , transfer, custom package
    timestamp = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=INTEREST_STATUS_CHOICES)
    device_info = models.CharField(max_length=255, blank=True, null=True)
    session_data = models.JSONField(blank=True, null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    objects = SoftDeleteManager()  # Custom manager
    all_objects = models.Manager()  # Default manager to access all records, including deleted
    

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
        return f'Interest {self.interest_id} by User {self.user_id}'

    class Meta:
        ordering = ['-timestamp']

