from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from role.models import Role
import uuid
from login.models import CustomUser

from django.utils import timezone


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
    
    


class RolePerUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)  
    users = models.ManyToManyField(User, related_name='roles')
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
        # Return a string representation of the Role and the list of users
        user_names = ", ".join([user.username for user in self.users.all()])
        return f'Role: {self.role.name}, Users: {user_names}'
    
    
class RolePerClient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)  
    clients = models.ManyToManyField(CustomUser, related_name='roles')
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
        client_usernames = ", ".join([client.fullName for client in self.clients.all()])
        return f'Role: {self.role.name}, Clients: {client_usernames}'

 
   