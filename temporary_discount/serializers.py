from rest_framework import serializers
from .models import TempoararyDiscount,PromotionCode

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempoararyDiscount
        fields = '__all__'
        
        
class PromotionCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionCode
        fields = '__all__'