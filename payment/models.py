from django.db import models

# Create your models here.


    
    
class Payment(models.Model):
    ACTION_CHOICES = [
        ('SALE', 'Sale'),
        ('3DS', '3D Secure'),
        ('REDIRECT', 'Redirect'),
        ('REFUND', 'Refund'),
        ('RECURRING', 'Recurring'),
        ('sale','Sale'),
        ('refund','Refund')
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
    
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    result = models.CharField(max_length=50, choices=RESULT_CHOICES)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, blank=True, null=True)
    order_id = models.CharField(max_length=100)
    trans_id = models.CharField(max_length=100)
    trans_date = models.DateTimeField(null=True, blank=True)
    descriptor = models.CharField(max_length=255, blank=True, null=True)
    recurring_token = models.CharField(max_length=255, blank=True, null=True)
    schedule_id = models.CharField(max_length=255, blank=True, null=True)
    card_token = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10)
    decline_reason = models.TextField(blank=True, null=True)
    redirect_url = models.URLField(blank=True, null=True)
    redirect_params = models.JSONField(blank=True, null=True)
    redirect_method = models.CharField(max_length=10, blank=True, null=True)
    card = models.CharField(max_length=255, blank=True, null=True)
    card_expiration_date = models.CharField(max_length=10, blank=True, null=True)
    hash = models.CharField(max_length=255, blank=True, null=True)
    source = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return f"{self.action} - {self.status} - {self.order_id}"
   
    
    
    
