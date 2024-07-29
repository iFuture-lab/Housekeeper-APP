from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import HireRequest

@receiver(post_save, sender=HireRequest)
def update_housekeeper_availability(sender, instance, **kwargs):
    if instance.status.Status == "Approved":
        housekeeper = instance.housekeeper
        housekeeper.is_available = False
        housekeeper.save()
        
        print(f"Housekeeper {housekeeper.Name} availability set to False")
    else:
        print(f"HireRequest {instance.id} status is {instance.status.Status}")


       