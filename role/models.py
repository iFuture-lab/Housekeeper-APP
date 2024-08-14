from django.db import models
import uuid

# Create your models here.



class Permission(models.Model):
    name = models.CharField(max_length=100, unique=True)  # e.g., "can_delete_role"

    def __str__(self):
        return self.name


class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(unique=True,max_length=50)
    
    permissions = models.ManyToManyField(Permission, related_name='roles')


    def __str__(self):
        return self.name
    
    

