from rest_framework import serializers
from .models import Contract


from .models import UserInterest

class UserInterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInterest
        fields = '__all__'

    def create(self, validated_data):
        return UserInterest.objects.create(**validated_data)
  
        

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'
        read_only_fields = ('contract_number',)
        
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('deleted_at', None)
        
        