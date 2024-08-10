from django.db import models
import uuid

# Create your models here.
class Nationallity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Nationality= models.CharField(max_length=150,)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.Nationality
 