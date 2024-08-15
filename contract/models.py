from django.db import models
import uuid
from login.models import CustomUser
from payment.models import Payment
from temporary_discount.models import CustomPackage
from service_type.models import ServiceType

from django.db.models.functions import Cast
from django.db.models import IntegerField


class Contract(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contract_number = models.CharField(max_length=5, unique=True, blank=True)
    customer_id = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    package_details = models.ForeignKey(CustomPackage,on_delete=models.CASCADE,null=True)
    payment_details = models.ForeignKey(Payment,on_delete=models.CASCADE,null=True)
    contract_terms = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed')])
    request_type = models.ForeignKey(ServiceType,on_delete=models.CASCADE,null=True)

    def save(self, *args, **kwargs):
        if not self.contract_number:
            self.contract_number = self.generate_contract_number()
        super().save(*args, **kwargs)

    def generate_contract_number(self):
        # Convert contract_number to integers, ignoring non-numeric values
        last_contract = Contract.objects.annotate(
            contract_num_as_int=Cast('contract_number', IntegerField())
        ).order_by('-contract_num_as_int').first()

        if not last_contract or not last_contract.contract_number.isdigit():
            return '00001'

        last_number = int(last_contract.contract_number)
        new_number = last_number + 1
        return str(new_number).zfill(5)
