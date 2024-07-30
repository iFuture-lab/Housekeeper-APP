from django.db import models
from login.models import CustomUser
from django.utils import timezone
from nationality.models import Nationallity
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import AppConfig




class Status(models.Model):
    Status= models.CharField(max_length=50)
    
    def __str__(self):
        return self.Status

    
    
class Housekeeper(models.Model):
    Name= models.CharField(max_length=50,)
    Age= models.IntegerField()
    nationality= models.ForeignKey(Nationallity, on_delete=models.CASCADE)  # Link to User model 
    isactive = models.BooleanField(default=True)  # Ensure parentheses are used
    is_available = models.BooleanField(default=True)  # Ensure parentheses are used
    worked_before = models.BooleanField(default=True)
    #pricePerMonth=models.FloatField(default=0.0)

    
    def __str__(self):
        return self.Name
    
    
class HireRequest(models.Model):
    housekeeper = models.ForeignKey(Housekeeper, on_delete=models.CASCADE, related_name='hire_requests',)
    requester = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Link to User model
    requester_contact = models.CharField(max_length=100)
    hire_duration=models.IntegerField
    request_date = models.DateField(default=timezone.now)  # Set default to today's date
    #status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')
    status= models.ForeignKey(Status, on_delete=models.CASCADE)  # Link to Status model
    
    def save(self, *args, **kwargs):
        if self.status is None:
            # Set default status if not set
            default_status, created = Status.objects.get_or_create(name='Pending')
            self.status = default_status
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Hire Request by {self.requester.fullName} for Housekeeper {self.housekeeper.Name}"
    
    ######################### update available ##################
# @receiver(post_save, sender=HireRequest)
# def update_housekeeper_availability(sender, instance, **kwargs):
#     if instance.status.Status == "Approved":
#         housekeeper = instance.housekeeper
#         housekeeper.is_available = False
#         housekeeper.save()
        
#         print(f"Housekeeper {housekeeper.Name} availability set to False")
#     else:
#         print(f"HireRequest {instance.id} status is {instance.status.Status}")



    
class RecruitmentRequest(models.Model):
    housekeeper = models.ForeignKey(Housekeeper, on_delete=models.CASCADE, related_name='recruitment_requests')
    requester = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Link to User model
    request_contact = models.CharField(max_length=100)
    recruitment_duration=models.IntegerField
    visa_status= models.BooleanField(default=False)
    requested_date = models.DateField(default=timezone.now) 
    #status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')
    status= models.ForeignKey(Status, on_delete=models.CASCADE,default='Pending')  # Link to Status model

    def __str__(self):
        return f"Recruitment Request by {self.requester.fullName} for Housekeeper {self.housekeeper.Name}"
    
    
class TransferRequest(models.Model):
    housekeeper = models.ForeignKey(Housekeeper, on_delete=models.CASCADE, related_name='transfer_requests')
    requester = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Link to User model
    # request_contact = models.CharField(max_length=100)
    requested_date = models.DateField(default=timezone.now) 
    status= models.ForeignKey(Status, on_delete=models.CASCADE,default='Pending')  # Link to Status model
    #status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')

    def __str__(self):
        return f"Transfer Request by {self.requester.fullName} for Housekeeper {self.housekeeper.Name}"
    
    
    


    
    
    
    
    
    
    

