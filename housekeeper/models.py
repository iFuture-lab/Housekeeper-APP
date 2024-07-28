from django.db import models
from login.models import CustomUser
from django.utils import timezone
from nationality.models import Nationallity


class Status(models.Model):
    Status= models.CharField(max_length=50)
    
    def __str__(self):
        return self.Status

    
    
class Housekeeper(models.Model):
    Name= models.CharField(max_length=50,)
    Age= models.IntegerField()
    nationality= models.ForeignKey(Nationallity, on_delete=models.CASCADE)  # Link to User model 
    isactive = models.BooleanField(default=True)  # Ensure parentheses are used
    is_available = models.BooleanField(default=False)  # Ensure parentheses are used
    #pricePerMonth=models.FloatField(default=0.0)

    
    def __str__(self):
        return self.Name
    
    
class HireRequest(models.Model):
    housekeeper = models.ForeignKey(Housekeeper, on_delete=models.CASCADE, related_name='hire_requests',)
    requester = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Link to User model
    requester_contact = models.CharField(max_length=100)
    request_date = models.DateField(default=timezone.now)  # Set default to today's date
    #status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')
    status= models.ForeignKey(Status, on_delete=models.CASCADE,)  # Link to Status model

    def __str__(self):
        return f"Hire Request by {self.requester.fullName} for Housekeeper {self.housekeeper.Name}"
    
    
class RecruitmentRequest(models.Model):
    housekeeper = models.ForeignKey(Housekeeper, on_delete=models.CASCADE, related_name='recruitment_requests')
    requester = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Link to User model
    request_contact = models.CharField(max_length=100)
    visa_status= models.BooleanField(default=False)
    requested_date = models.DateField(default=timezone.now) 
    #status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')
    status= models.ForeignKey(Status, on_delete=models.CASCADE,)  # Link to Status model

    def __str__(self):
        return f"Recruitment Request by {self.requester.fullName} for Housekeeper {self.housekeeper.Name}"
    
    
class TransferRequest(models.Model):
    housekeeper = models.ForeignKey(Housekeeper, on_delete=models.CASCADE, related_name='transfer_requests')
    requester = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Link to User model
    requested_date = models.DateField(default=timezone.now) 
    status= models.ForeignKey(Status, on_delete=models.CASCADE)  # Link to Status model
    #status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')

    def __str__(self):
        return f"Transfer Request by {self.requester.fullName} for Housekeeper {self.housekeeper.Name}"
    
    
    


    
    
    
    
    
    
    

