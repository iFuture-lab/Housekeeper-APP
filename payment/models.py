from django.db import models
import uuid
from housekeeper.models import HireRequest,RecruitmentRequest,TransferRequest
# Create your models here.
from django.utils import timezone



###################soft#################################################

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


    
    
class Payment(models.Model):
    
    
    hire_request = models.ForeignKey(HireRequest, blank=True, null=True, on_delete=models.CASCADE)
    transfer_request = models.ForeignKey(TransferRequest, blank=True, null=True, on_delete=models.CASCADE)
    recruitment_request = models.ForeignKey(RecruitmentRequest, blank=True, null=True, on_delete=models.CASCADE)




    
    ACTION_CHOICES = [
        ('SALE', 'Sale'),
        ('3DS', '3D Secure'),
        ('REDIRECT', 'Redirect'),
        ('REFUND', 'Refund'),
        ('RECURRING', 'Recurring'),
        ('sale','Sale'),
        ('refund','Refund'),
        ('GET_TRANS_DETAILS','GET_TRANS_DETAILS')
    ]
    
    RESULT_CHOICES = [
         ('SUCCESS', 'Success'),
        ('DECLINED', 'Declined'),
        ('REDIRECT', 'Redirect'),
        ('ACCEPTED', 'Accepted'),
        ('ERROR', 'Error'),
        ('',''),
    ]
    
    STATUS_CHOICES = [
        ('3DS', '3D Secure'),
        ('REDIRECT', 'Redirect'),
        ('SETTLED', 'Settled'),
        ('REFUND', 'Refund'),
        ('DECLINED', 'Declined'),
        ('PREPARE','Prepare'),
        ('PENDING','Pending'),
        ('success' ,'Success'),
        ('fail','Fail'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    action = models.CharField(max_length=50,blank=True, null=True)
    result = models.CharField(max_length=50,blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    order_id = models.CharField(max_length=100,blank=True, null=True)
    trans_id = models.CharField(max_length=100,blank=True, null=True)
    trans_date = models.DateTimeField(null=True, blank=True)
    descriptor = models.CharField(max_length=255, blank=True, null=True)
    recurring_token = models.CharField(max_length=255, blank=True, null=True)
    schedule_id = models.CharField(max_length=255, blank=True, null=True)
    card_token = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10,blank=True, null=True)
    decline_reason = models.TextField(blank=True, null=True)
    redirect_url = models.URLField(blank=True, null=True)
    redirect_params = models.JSONField(blank=True, null=True)
    redirect_method = models.CharField(max_length=10, blank=True, null=True)
    card = models.CharField(max_length=255, blank=True, null=True)
    card_expiration_date = models.CharField(max_length=10, blank=True, null=True)
    hash = models.CharField(max_length=255, blank=True, null=True)
    source = models.CharField(max_length=50, blank=True, null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    
    objects = SoftDeleteManager()  
    all_objects = models.Manager()  

    def delete(self):
      
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
    
        self.deleted_at = None
        self.save()

    def hard_delete(self):
      
        super().delete()


    
    
    
    
    def __str__(self):
        return f"{self.action} - {self.status} - {self.order_id}"
   
    
    
    
