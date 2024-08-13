# from django.db import models
# from nationality.models import Nationallity
# from service_type.models import ServiceType
from housekeeper import models

from django.db import models
from nationality.models import Nationallity
from service_type.models import ServiceType
import uuid
# Create your models here.

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
    
    
    
