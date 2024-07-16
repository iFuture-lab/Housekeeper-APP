from django.db import models

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


