from django.db import models

# Create your models here.


class Role(models.Model):
    name = models.CharField(unique=True,max_length=50)    


    def __str__(self):
        return self.name
