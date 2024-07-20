from django.db import models
from django.contrib.auth.models import User

# Create your models here.# login/models.py


class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)  # Ensure you hash passwords properly
    password2 = models.CharField(max_length=128)  # Ensure you hash passwords properly
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    


    def __str__(self):
        return self.username
    
class HousekeeperRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request_date = models.DateField(auto_now_add=True)
    service_type = models.CharField(max_length=100)
    additional_notes = models.TextField(blank=True)
    nationality = models.CharField(max_length=50,)

    def __str__(self):
        return f"Request from {self.user.username} on {self.request_date}"

    
    


