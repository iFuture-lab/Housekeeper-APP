from rest_framework import serializers
from .models import Housekeeper, HireRequest, RecruitmentRequest, TransferRequest
from login.models import CustomUser

class HousekeeperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Housekeeper
        fields = ['id', 'Name', 'Age', 'nationality', 'isactive', 'isvailability', 'pricePerMonth']

class HireRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = HireRequest
        fields = ['id', 'housekeeper', 'requester', 'requester_contact', 'request_date', 'status']

class RecruitmentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecruitmentRequest
        fields = ['id', 'housekeeper', 'requester', 'request_contact', 'visa_status', 'requested_date', 'status']

class TransferRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferRequest
        fields = ['id', 'housekeeper', 'requester', 'requested_date', 'status']
        
class HousekeeperIDSerializer(serializers.Serializer):
    id = serializers.IntegerField()
