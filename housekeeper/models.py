
from django.db import models
from django.utils import timezone
from login.models import CustomUser
from nationality.models import Nationallity
from service_type.models import ServiceType
from perice_per_nationality.models import PericePerNationality
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth import get_user_model
import uuid
from temporary_discount.models import TempoararyDiscount

User = get_user_model()




class ActionLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    action_type = models.CharField(max_length=255)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.timestamp} - {self.action_type} by {self.user}"


class Status(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Status= models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.Status
    
class Religion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    
class EmploymentType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    
    
class Housekeeper(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Name= models.CharField(max_length=50,)
    Age= models.IntegerField()
    gender_CHOICES = {
    "female": "Female",
    "male": "Male",
}
    gender=models.CharField(max_length=50,choices=gender_CHOICES,default='female')
    nationality= models.ForeignKey(Nationallity, on_delete=models.CASCADE)  
    religion= models.ForeignKey(Religion,on_delete=models.CASCADE,null=True)
    isactive = models.BooleanField(default=True)  #
    is_available = models.BooleanField(default=True)  # Ensure parentheses are used
    worked_before = models.BooleanField(default=True)
    employment_type = models.ForeignKey(EmploymentType,on_delete=models.CASCADE,null=True)
    experience_years = models.IntegerField()  
    languages_spoken = models.JSONField() 
    rating = models.FloatField() 
    request_types= models.ManyToManyField(ServiceType, through='HousekeeperRequestType',related_name='housekeeper')
    

    
    def __str__(self):
        return self.Name
    
    
    
class HousekeeperRequestType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    housekeeper = models.ForeignKey(Housekeeper, on_delete=models.CASCADE)
    request_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('housekeeper', 'request_type')  # Ensure unique pairs

    def __str__(self):
        return f"{self.housekeeper.Name} - {self.request_type.name}"
    
    

    
    
class HireRequest(models.Model):
    
    
    def get_default_service_type():
        return ServiceType.objects.get(name='Hire')  

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    readonly_fields = ('pericepernationality_id',)
    housekeeper = models.ForeignKey(Housekeeper, on_delete=models.CASCADE, related_name='hire_requests',)
    requester = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Link to User model
    requester_contact = models.CharField(max_length=100)
    request_date = models.DateField(default=timezone.now) 
    requester_firstName = models.CharField(max_length=100,default='DefaultFirstName') 
    requester_lastName = models.CharField(max_length=100,default='DefaultLastName')   
    requester_city = models.CharField(max_length=100,null=True) 
    duration=models.IntegerField(default=1)
    pericepernationality_id = models.ForeignKey(PericePerNationality, on_delete=models.CASCADE,null=True)
    total_price =models.FloatField(default=0.0)
    status= models.ForeignKey(Status, on_delete=models.CASCADE)
    temporary_discount = models.ForeignKey(TempoararyDiscount, null=True, on_delete=models.CASCADE)
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE,null=True,default=get_default_service_type)
    
    
    def save(self, *args, **kwargs):
        if self.status is None:
            default_status, created = Status.objects.get_or_create(name='Pending')
            self.status = default_status

        # Automatically set pericepernationalit_id based on housekeeper's details
        if self.housekeeper:
            try:
                perice_per_nationality = PericePerNationality.objects.get(
                    nationality=self.housekeeper.nationality,
                    service_type=self.service_type,  # Adjust this according to your service type field or logic
                    employment_type=self.housekeeper.employment_type,
                    worked_before=self.housekeeper.worked_before
                    # Filter based on worked_before if applicable
                    
                )
                self.pericepernationalit_id = perice_per_nationality
                self.total_price = self.duration * perice_per_nationality.fees
                print("hiiiiiiiiiiiiiiiiiii")
                # Apply discount if available
              
                
            except PericePerNationality.DoesNotExist:
                self.pericepernationality_id = None
                self.total_price=0.0
                
            # # Raise a validation error to be caught and displayed
            #     raise ValidationError('No matching PericePerNationality found. Please ensure the PericePerNationality is set correctly.')

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Hire Request by {self.requester.fullName} for Housekeeper {self.housekeeper.Name}"
    

    
class RecruitmentRequest(models.Model):
    
    # default_service_type = ServiceType.objects.get(name='Recruitment') 
    
    def get_default_service_type():
        return ServiceType.objects.get(name='Recruitment') 
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    housekeeper = models.ForeignKey(Housekeeper, on_delete=models.CASCADE, related_name='recruitment_requests')
    requester = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Link to User model
    request_contact = models.CharField(max_length=100)
    recruitment_duration=models.IntegerField
    visa_status= models.BooleanField(default=False)
    requested_date = models.DateField(default=timezone.now) 
    #status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')
    status= models.ForeignKey(Status, on_delete=models.CASCADE,default='Pending')  # Link to Status model
    temporary_discount = models.ForeignKey(TempoararyDiscount, null=True, on_delete=models.CASCADE)
    pericepernationality_id = models.ForeignKey(PericePerNationality, on_delete=models.CASCADE,null=True)
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE,null=True,default=get_default_service_type)
    total_price =models.FloatField(default=0.0)
    

    def save(self, *args, **kwargs):
        if self.status is None:
            default_status, created = Status.objects.get_or_create(name='Pending')
            self.status = default_status

        # Automatically set pericepernationalit_id based on housekeeper's details
        if self.housekeeper:
            try:
                perice_per_nationality = PericePerNationality.objects.get(
                    nationality=self.housekeeper.nationality,
                    service_type=self.service_type,  
                    employment_type=self.housekeeper.employment_type,
                    worked_before=self.housekeeper.worked_before
                    # Filter based on worked_before if applicable
                    
                )
                self.pericepernationalit_id = perice_per_nationality
                self.total_price = perice_per_nationality.fees
                print("hiiiiiiiiiiiiiiiiiii")
              
            
                
            except PericePerNationality.DoesNotExist:
                self.pericepernationality_id = None
                self.total_price=0.0
                
            # # Raise a validation error to be caught and displayed
            #     raise ValidationError('No matching PericePerNationality found. Please ensure the PericePerNationality is set correctly.')

               
    
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Recruitment Request by {self.requester.fullName} for Housekeeper {self.housekeeper.Name}"
    
    
class TransferRequest(models.Model):
    default_service_type = ServiceType.objects.get(name='Transfer')
    def get_default_service_type():
        return ServiceType.objects.get(name='Transfer') 
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    housekeeper = models.ForeignKey(Housekeeper, on_delete=models.CASCADE, related_name='transfer_requests')
    requester = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Link to User model
    requested_date = models.DateField(default=timezone.now) 
    request_contact = models.CharField(max_length=100,default='0123456789')
    status= models.ForeignKey(Status, on_delete=models.CASCADE,default='Pending') 
    requester_firstName = models.CharField(max_length=100,default='DefaultFirstName') 
    requester_lastName = models.CharField(max_length=100,default='DefaultLastName')   
    requester_city = models.CharField(max_length=100,null=True) 
    temporary_discount = models.ForeignKey(TempoararyDiscount, null=True, on_delete=models.CASCADE)
    pericepernationality_id = models.ForeignKey(PericePerNationality, on_delete=models.CASCADE,null=True)
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE,null=True,default=get_default_service_type)
    total_price =models.FloatField(default=0.0)
    
    def save(self, *args, **kwargs):
        if self.status is None:
            default_status, created = Status.objects.get_or_create(name='Pending')
            self.status = default_status

        # Automatically set pericepernationalit_id based on housekeeper's details
        if self.housekeeper:
            try:
                perice_per_nationality = PericePerNationality.objects.get(
                    nationality=self.housekeeper.nationality,
                    service_type=self.service_type,  
                    employment_type=self.housekeeper.employment_type,
                    worked_before=self.housekeeper.worked_before
                    # Filter based on worked_before if applicable
                    
                )
                self.pericepernationalit_id = perice_per_nationality
                self.total_price = perice_per_nationality.fees
                print("hiiiiiiiiiiiiiiiiiii")
                
             
                
            except PericePerNationality.DoesNotExist:
                self.pericepernationality_id = None
                self.total_price=0.0
                
            # # Raise a validation error to be caught and displayed
            #     raise ValidationError('No matching PericePerNationality found. Please ensure the PericePerNationality is set correctly.')

 

        super().save(*args, **kwargs)


    def __str__(self):
        return f"Transfer Request by {self.requester.fullName} for Housekeeper {self.housekeeper.Name}"
    

    
    


    
    
    
    
    
    
    

