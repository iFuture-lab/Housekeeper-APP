from django.db import models
import uuid
from django.utils import timezone

# Create your models here.

##################soft###################################

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
    
    
    
class Nationallity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Nationality= models.CharField(max_length=150,)
    is_active = models.BooleanField(default=True)
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
        return self.Nationality
 