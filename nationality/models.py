from django.db import models

# Create your models here.
class Nationallity(models.Model):
    Nationality= models.CharField(max_length=150,)
    
    def __str__(self):
        return self.Nationality
 