
from django.db import models
from django.utils import timezone
from login.models import CustomUser
from nationality.models import Nationallity
from service_type.models import ServiceType
from perice_per_nationality.models import PericePerNationality
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()




class ActionLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    action_type = models.CharField(max_length=255)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp} - {self.action_type} by {self.user}"


class Status(models.Model):
    Status= models.CharField(max_length=50)
    
    def __str__(self):
        return self.Status
    
class Religion(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    
class EmploymentType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    
    
class Housekeeper(models.Model):
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
    worked_before_salary= models.FloatField(null=True, blank=True)
    employment_type = models.ForeignKey(EmploymentType,on_delete=models.CASCADE,null=True)
    # montly_salary = models.FloatField(default=0.0)
    # pricePerMonth=models.FloatField(default=0.0)

    
    def __str__(self):
        return self.Name
    
    # def save(self, *args, **kwargs):
    #     if not self.worked_before:
    #         self.worked_before_salary = None  # Ensure the field is cleared if worked_before is False

    #     self.monthly_salary = self.calculate_monthly_salary()
    #     super(Housekeeper, self).save(*args, **kwargs)
        
    
    
    
    
class HireRequest(models.Model):
    
    readonly_fields = ('pericepernationality_id',)
    housekeeper = models.ForeignKey(Housekeeper, on_delete=models.CASCADE, related_name='hire_requests',)
    requester = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Link to User model
    requester_contact = models.CharField(max_length=100)
    request_date = models.DateField(default=timezone.now)  # Set default to today's date
    duration=models.IntegerField(default=1)
    pericepernationality_id = models.ForeignKey(PericePerNationality, on_delete=models.CASCADE,null=True)
    total_price =models.FloatField(default=0.0)
    status= models.ForeignKey(Status, on_delete=models.CASCADE)  # Link to Status model
    
    def save(self, *args, **kwargs):
        # Automatically set pericepernationalit_id based on housekeeper's details
        if self.housekeeper:
            try:
                perice_per_nationality = PericePerNationality.objects.get(
                    nationality=self.housekeeper.nationality,
                    service_type=1,  # Adjust this according to your service type field or logic
                    employment_type=self.housekeeper.employment_type,
                    worked_before=self.housekeeper.worked_before
                    # Filter based on worked_before if applicable
                    # You may need to adjust based on how 'worked_before' is handled
                )
                self.pericepernationalit_id = perice_per_nationality
                self.total_price = self.duration * perice_per_nationality.price
                print("hiiiiiiiiiiiiiiiiiii")
            
                
            except PericePerNationality.DoesNotExist:
            # Raise a validation error to be caught and displayed
                raise ValidationError('No matching PericePerNationality found. Please ensure the PericePerNationality is set correctly.')

   
               
        if self.status is None:
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
    
    
    


    
    
    
    
    
    
    

