from rest_framework import serializers
from .models import PericePerNationality



    
        

class PericePerNationalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PericePerNationality
        fields = '__all__'
        
        
