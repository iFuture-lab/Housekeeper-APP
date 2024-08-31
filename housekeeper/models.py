
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
from temporary_discount.models import TempoararyDiscount,CustomPackage
from django.utils import timezone
from django.core.validators import RegexValidator
from decimal import Decimal



User = get_user_model()
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
    
    




class ActionLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    custom_user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    action_type = models.CharField(max_length=255)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    

    def __str__(self):
        return f"{self.timestamp} - {self.action_type} by {self.user} or {self.custom_user}"
    
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
        
        
class Taxes(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name= models.CharField(max_length=50,unique=True)
    amount= models.FloatField()
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
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
        return self.name


class Status(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Status= models.CharField(max_length=50,unique=True)
    is_active = models.BooleanField(default=True)
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
        return self.Status
    
class Religion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100,unique=True)
    is_active = models.BooleanField(default=True)
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
        return self.name
    
    
class EmploymentType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100,unique=True)
    is_active = models.BooleanField(default=True)
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
        return self.name
    

    def __str__(self):
        return self.name

    
    
class Housekeeper(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Name= models.CharField(max_length=50)
    Age= models.IntegerField()
    gender_CHOICES = {
    "female": "Female",
    "male": "Male",
}
    gender=models.CharField(max_length=50,choices=gender_CHOICES,default='female')
    nationality= models.ForeignKey(Nationallity, on_delete=models.CASCADE,null=True)  
    religion= models.ForeignKey(Religion,on_delete=models.CASCADE,null=True)
    isactive = models.BooleanField(default=True)  
    is_available = models.BooleanField(default=True)  
    worked_before = models.BooleanField(default=True)
    Identification_number=models.CharField(max_length=150,unique=True)
    employment_type = models.ForeignKey(EmploymentType,on_delete=models.CASCADE,null=True)
    experience_years = models.IntegerField(null=True,blank=True)  
    languages_spoken = models.JSONField(null=True,blank=True) 
    rating = models.FloatField(null=True,blank=True) 
    request_types= models.ManyToManyField(ServiceType, through='HousekeeperRequestType',related_name='housekeeper')
    deleted_at = models.DateTimeField(null=True, blank=True)
    
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
        return self.name
    
    # def save(self, *args, **kwargs):
    #     if Housekeeper.objects.filter(Name=self.Name).exists():
    #         raise ValidationError(f'A housekeeper with the name "{self.Name}" already exists.')
    #     super().save(*args, **kwargs)
    
    

    
    def __str__(self):
        return self.Name
    
    
    
class HousekeeperRequestType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    housekeeper = models.ForeignKey(Housekeeper, on_delete=models.CASCADE)
    request_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    
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
        return self.name
    
    deleted_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        unique_together = ('housekeeper', 'request_type')  

    def __str__(self):
        return f"{self.housekeeper.Name} - {self.request_type.name}"
    
    

    
    
class HireRequest(models.Model):
    
    def get_current_date():
        return timezone.now().date()
    
    def get_default_service_type():
        return ServiceType.objects.get(name='Hire')  
    
    def get_default_status():
        return Status.objects.get(Status='Pending')
    
    def get_default_taxes():
        return Taxes.objects.get(name='default')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    readonly_fields = ('pericepernationality_id',)
    housekeeper = models.ForeignKey(Housekeeper, on_delete=models.CASCADE, related_name='hire_requests',)
    requester = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Link to User model
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="contact numbber must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    requester_contact = models.CharField(validators=[phone_regex],max_length=17)
    request_date = models.DateField(default=get_current_date)
    requester_firstName = models.CharField(max_length=100,) 
    requester_lastName = models.CharField(max_length=100,)  
    requester_fatherName = models.CharField(max_length=100,) 
    requester_city = models.CharField(max_length=100,) 
    duration=models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    price=models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    # status= models.ForeignKey(Status, on_delete=models.CASCADE,blank=True)  # Link to Status model
    status = models.ForeignKey(Status, on_delete=models.CASCADE, default=get_default_status,blank=True)
    temporary_discount = models.ForeignKey(TempoararyDiscount, null=True, on_delete=models.CASCADE,blank=True)
    custom_package_id = models.ForeignKey(CustomPackage, on_delete=models.CASCADE,null=True,blank=True)
    request_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE,null=True,default=get_default_service_type)
    order_id = models.CharField(max_length=255, unique=True, blank=True, null=True) 
    deleted_at = models.DateTimeField(null=True, blank=True)
    tax_id = models.ForeignKey(Taxes, null=True, on_delete=models.CASCADE,blank=True,default=get_default_taxes)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    
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
        return self.name
    
    
    
    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = f"{self.id}-{uuid.uuid4().hex[:8]}"
            
       

        if self.housekeeper:
            try:
                perice = CustomPackage.objects.get(
                    nationallities=self.housekeeper.nationality,
                    request_type=self.request_type, 
                    employment_type=self.housekeeper.employment_type,
                    
                    
                )
                
                print(perice.final_price)
                
                self.price=perice.final_price
                
                add_tax = Decimal(0)  

                if self.tax_id:
                    tax = Decimal(self.tax_id.amount)
                    tax_fraction = tax / Decimal(100)
                    print(tax_fraction)
                    add_tax = perice.final_price * tax_fraction  
                    print(add_tax)
                    self.tax_amount=add_tax
                    
                total_perice = perice.final_price + add_tax  
                self.total_price = total_perice
                print("hiiiiiiiiiiiiiiiiiii")
               
                
            except CustomPackage.DoesNotExist:
                print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
                self.custom_package_id = None
                self.total_price=0.0
                
           
            #     raise ValidationError('No matching PericePerNationality found. Please ensure the PericePerNationality is set correctly.')

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Hire Request by {self.requester.fullName} for Housekeeper {self.housekeeper.Name}"
    

    
class RecruitmentRequest(models.Model):
    
    # default_service_type = ServiceType.objects.get(name='Recruitment') 
    
    def get_default_service_type():
        return ServiceType.objects.get(name='Recruitment') 
    
    def get_current_date():
        return timezone.now().date()
    
    def get_default_status():
        return Status.objects.get(Status='Pending')
    
    
    def get_default_taxes():
        return Taxes.objects.get(name='default')
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    housekeeper = models.ForeignKey(Housekeeper, on_delete=models.CASCADE, related_name='recruitment_requests')
    requester = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="contact numbber must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    requester_contact = models.CharField(validators=[phone_regex], max_length=17,)
    visa_status= models.BooleanField(default=False)
    request_date = models.DateField(default=get_current_date)
    requester_firstName = models.CharField(max_length=100,) 
    requester_lastName = models.CharField(max_length=100,)
    requester_fatherName = models.CharField(max_length=100,)    
    requester_city = models.CharField(max_length=100,)    
    #status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')
    # status= models.ForeignKey(Status, on_delete=models.CASCADE,blank=True)  # Link to Status model
    status = models.ForeignKey(Status, on_delete=models.CASCADE, default=get_default_status,blank=True)
    temporary_discount = models.ForeignKey(TempoararyDiscount, null=True, on_delete=models.CASCADE,blank=True)
    # pericepernationality_id = models.ForeignKey(PericePerNationality, on_delete=models.CASCADE,null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    price=models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    custom_package_id = models.ForeignKey(CustomPackage, on_delete=models.CASCADE,null=True,blank=True)
    request_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE,null=True,default=get_default_service_type)
    order_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    tax_id = models.ForeignKey(Taxes, null=True, on_delete=models.CASCADE,blank=True,default=get_default_taxes)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    
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
        return self.name
    
    
    
    def save(self, *args, **kwargs):
        

        if self.housekeeper:
            try:
                perice = CustomPackage.objects.get(
                    nationallities=self.housekeeper.nationality,
                    request_type=self.request_type, 
                    employment_type=self.housekeeper.employment_type,
                    
                    
                )
                
                self.price=perice.final_price
                
                add_tax = Decimal(0)  

                if self.tax_id:
                    tax = Decimal(self.tax_id.amount)
                    tax_fraction = tax / Decimal(100)
                    print(tax_fraction)
                    add_tax = perice.final_price * tax_fraction  
                    print(add_tax)
                    self.tax_amount=add_tax
                    
                

                total_perice = perice.final_price + add_tax  
                self.total_price = total_perice
                print("hiiiiiiiiiiiiiiiiiii i got ittttttttttttttttttttt")
            
                
            except CustomPackage.DoesNotExist:
                self.custom_package_id = None
                self.total_price=0.0
                
            # # Raise a validation error to be caught and displayed
            #     raise ValidationError('No matching PericePerNationality found. Please ensure the PericePerNationality is set correctly.')

        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Recruitment Request by {self.requester.fullName} for Housekeeper {self.housekeeper.Name} "
    
    
class TransferRequest(models.Model):
    #default_service_type = ServiceType.objects.get(name='Transfer')
    def get_default_service_type():
        return ServiceType.objects.get(name='Transfer') 
    
    def get_current_date():
        return timezone.now().date()
    
    def get_default_status():
        return Status.objects.get(Status='Pending')
     
    
    def get_default_taxes():
        return Taxes.objects.get(name='default')
    
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    housekeeper = models.ForeignKey(Housekeeper, on_delete=models.CASCADE, related_name='transfer_requests')
    requester = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Link to User model
    request_date = models.DateField(default=get_current_date) 
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="contact numbber must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    requester_contact = models.CharField(validators=[phone_regex], max_length=17,)
    # status= models.ForeignKey(Status, on_delete=models.CASCADE,blank=True)  # Link to Status model
    status = models.ForeignKey(Status, on_delete=models.CASCADE, default=get_default_status,blank=True)
    requester_firstName = models.CharField(max_length=100,) 
    requester_lastName = models.CharField(max_length=100,)  
    requester_fatherName = models.CharField(max_length=100,) 
    requester_city = models.CharField(max_length=100,) 
    temporary_discount = models.ForeignKey(TempoararyDiscount, null=True, on_delete=models.CASCADE,blank=True)
    # pericepernationality_id = models.ForeignKey(PericePerNationality, on_delete=models.CASCADE,null=True)
    # service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE,null=True,default=get_default_service_type)
    total_price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    price=models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    custom_package_id = models.ForeignKey(CustomPackage, on_delete=models.CASCADE,null=True,blank=True)
    request_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE,null=True,default=get_default_service_type)
    order_id = models.CharField(max_length=255, unique=True, blank=True, null=True) 
    deleted_at = models.DateTimeField(null=True, blank=True)
    tax_id = models.ForeignKey(Taxes, null=True, on_delete=models.CASCADE,blank=True,default=get_default_taxes)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    
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
        return self.name
    
    
    
    def save(self, *args, **kwargs):
       

        if self.housekeeper:
            try:
                perice = CustomPackage.objects.get(
                    nationallities=self.housekeeper.nationality,
                    request_type=self.request_type, 
                    employment_type=self.housekeeper.employment_type,
                    
                    
                )
                
                self.price=perice.final_price
                
                add_tax = Decimal(0)  

                if self.tax_id:
                    tax = Decimal(self.tax_id.amount)
                    tax_fraction = tax / Decimal(100)
                    print(tax_fraction)
                    add_tax = perice.final_price * tax_fraction  
                    print(add_tax)
                    self.tax_amount=add_tax
                    
                

                total_perice = perice.final_price + add_tax  
                self.total_price = total_perice
                print("hiiiiiiiiiiiiiiiiiii")
            
              
                
            except CustomPackage.DoesNotExist:
                self.custom_package_id = None
                self.total_price=0.0
                
            # # Raise a validation error to be caught and displayed
            #     raise ValidationError('No matching PericePerNationality found. Please ensure the PericePerNationality is set correctly.')

        super().save(*args, **kwargs)
    
    

    def __str__(self):
        return f"Transfer Request by {self.requester.fullName} for Housekeeper {self.housekeeper.Name}"
    

    
    


    
    
    
    
    
    
    

