from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from role.models import Role
import uuid
from login.models import CustomUser


class RolePerUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)  
    users = models.ManyToManyField(User, related_name='roles')

    def __str__(self):
        # Return a string representation of the Role and the list of users
        user_names = ", ".join([user.username for user in self.users.all()])
        return f'Role: {self.role.name}, Users: {user_names}'
    
    
class RolePerClient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)  
    clients = models.ManyToManyField(CustomUser, related_name='roles')
    
    
    def __str__(self):
        client_usernames = ", ".join([client.fullName for client in self.clients.all()])
        return f'Role: {self.role.name}, Clients: {client_usernames}'

 
   