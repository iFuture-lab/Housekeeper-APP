# from django.db import models
# from nationality.models import Nationallity
# from service_type.models import ServiceType
from housekeeper import models

from django.db import models
from nationality.models import Nationallity
from service_type.models import ServiceType
# Create your models here.

class PericePerNationality(models.Model):
    nationality=models.ForeignKey(Nationallity,on_delete=models.CASCADE)
    service_type= models.ForeignKey(ServiceType,on_delete=models.CASCADE)
    employment_type = models.ForeignKey('housekeeper.EmploymentType',on_delete=models.CASCADE,null=True)
    worked_before = models.BooleanField(default=True)
    price=models.FloatField(default=0.0)
    
    
