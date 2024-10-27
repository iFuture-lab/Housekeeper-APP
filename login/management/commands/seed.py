from typing import Any
from django.core.management.base import BaseCommand
from login.models import CustomUser
from login.serializers import RegisterSerializercustomer
from datetime import date

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        if not CustomUser.objects.filter(phone_number='966123456789').exists():
            user = CustomUser.objects.create(phone_number='966123456789', fullName='test_account_2', is_confirmed=True)
            user.set_password("test@123")
            user.save()
            self.stdout.write(self.style.SUCCESS('Database successfully seeded!'))
        else:
            self.stdout.write(self.style.WARNING('Data already exists in the database.'))