# serializers.py

from rest_framework import serializers
from .models import HousekeeperRequest

class HousekeeperRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = HousekeeperRequest
        fields = ['id', 'user', 'request_date', 'nationality', 'service_type']
