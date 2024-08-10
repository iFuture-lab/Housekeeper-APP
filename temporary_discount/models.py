from django.db import models
from perice_per_nationality.models import PericePerNationality
import uuid

# Create your models here.
class TempoararyDiscount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    price_per_nationality = models.ForeignKey(PericePerNationality, on_delete=models.CASCADE)
    discount_percentage = models.FloatField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Discount {self.id} - {self.discount_percentage}%"
    
    
class PromotionCode(models.Model):
    id = models.BigAutoField(primary_key=True)
    price_per_nationality = models.ForeignKey(PericePerNationality, on_delete=models.CASCADE)
    code = models.CharField(max_length=255)
    discount_percentage = models.FloatField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.code