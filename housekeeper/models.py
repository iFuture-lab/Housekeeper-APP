from django.db import models

class Housekeeper(models.Model):
    Name= models.CharField(max_length=50,)
    Age= models.IntegerField()
    nationality= models.CharField(max_length=50,)
    service_choices=(('Cleaing','Cleaning'),('Cooking','Cooking'),('Cleaning & Cooking','Cleaning & Cooking'),('Nanny','Nanny'))
    service_type= models.CharField(max_length=20,choices=service_choices)
    isactive= models.BooleanField

    
    
    def __str__(self):
        return f"Housekeeper Request #{self.id} by {self.Name}"
