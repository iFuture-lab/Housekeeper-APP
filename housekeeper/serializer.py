from rest_framework import serializers
from .models import Housekeeper, HireRequest, RecruitmentRequest, TransferRequest
from login.models import CustomUser




####################updating Status#####################################

class UpdateHireRequest(serializers.ModelSerializer):
    class Meta:
        model = HireRequest
        #ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)
        fields = ['status','id']


class DeleteHousekeeper(serializers.ModelSerializer):
    class Meta:
        model = Housekeeper
        fields=['id']
    
    

class DeleteHireRequest(serializers.ModelSerializer):
    class Meta:
        model = HireRequest
        fields=['id']
        

class DeleteRecruitmentRequest(serializers.ModelSerializer):
    class Meta:
        model = RecruitmentRequest
        fields=['id']
        

class DeleteTransferRequest(serializers.ModelSerializer):
    class Meta:
        model = TransferRequest
        fields=['id']

class DummyHousekeeperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Housekeeper
        fields = ['id']  # Add fields as needed
        
class DummyHireHousekeeperSerializer(serializers.ModelSerializer):
    class Meta:
        model = HireRequest
        fields = ['id']  # Add fields as needed
        
class DummyTransferRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferRequest
        fields = ['id']  # Add fields as needed
        
class DummyRecruitmentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecruitmentRequest
        fields = ['id']  # Add fields as needed

class HousekeeperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Housekeeper
        fields = ['id', 'Name', 'Age', 'nationality', 'isactive', 'is_available',]

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
