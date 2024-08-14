from django.db import models
from perice_per_nationality.models import PericePerNationality
import uuid
from nationality.models import Nationallity
from service_type.models import ServiceType
from django.utils import timezone


# Create your models here.
class TempoararyDiscount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # price_per_nationality = models.ForeignKey(PericePerNationality, on_delete=models.CASCADE)
    discount_percentage = models.FloatField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Discount {self.id} - {self.discount_percentage}%"
    
class CustomPackage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    #nationality = models.ForeignKey(Nationallity, on_delete=models.CASCADE, related_name='custom_packages')
    request_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE, related_name='custom_packages')
    final_price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    temporary_discount = models.ForeignKey(TempoararyDiscount, null=True, on_delete=models.CASCADE)
    is_discount = models.BooleanField(default=False)
    is_indefinitely = models.BooleanField(default=False)
    nationallities = models.ManyToManyField(Nationallity, through='CustomPackageNationallity',related_name='custom_packages')
    employment_type = models.ForeignKey('housekeeper.EmploymentType',on_delete=models.CASCADE,null=True)
    worked_before_salary = models.FloatField(null=True)  
    new_housekeeper_salary = models.FloatField(null=True)
    
    
    

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Ensure that end_date is set to None if the package is indefinitely available
        if self.is_indefinitely:
            self.end_date = None
        super().save(*args, **kwargs)
        
        
class CustomPackageNationallity(models.Model):
    custom_package = models.ForeignKey(CustomPackage, on_delete=models.CASCADE, related_name='custom_package_nationallities')
    nationallity = models.ForeignKey(Nationallity, on_delete=models.CASCADE,related_name='custom_package_nationallities')
    
    class Meta:
        unique_together = ('custom_package', 'nationallity')
        
    def __str__(self):
        return self.custom_package.name
        
    
    
class PromotionCode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    price_per_nationality = models.ForeignKey(PericePerNationality, on_delete=models.CASCADE)
    code = models.CharField(max_length=255)
    discount_percentage = models.FloatField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.code