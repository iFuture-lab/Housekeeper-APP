
# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class HousekeeperRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request_date = models.DateField(auto_now_add=True)
    service_type = models.CharField(max_length=100)
    additional_notes = models.TextField(blank=True)
    nationality = models.CharField(max_length=50,)
    
    
    def __str__(self):
        return f"Housekeeper Request #{self.id} by {self.user.username}"
