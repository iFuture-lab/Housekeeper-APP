# from django.db import models
# from nationality.models import Nationallity
# from service_type.models import ServiceType
from housekeeper import models

from django.db import models
from nationality.models import Nationallity
from service_type.models import ServiceType
import uuid
from django.utils import timezone
# Create your models here.

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
    

class PericePerNationality(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nationality=models.ForeignKey(Nationallity,on_delete=models.CASCADE)
    service_type= models.ForeignKey(ServiceType,on_delete=models.CASCADE)
    employment_type = models.ForeignKey('housekeeper.EmploymentType',on_delete=models.CASCADE,null=True)
    worked_before = models.BooleanField(default=True)
    worked_before_salary = models.FloatField(null=True)  
    new_housekeeper_salary = models.FloatField(null=True)
    fees=models.FloatField(default=0.0)
    is_active = models.BooleanField(default=True)
    description=models.TextField()
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


    
    
    
