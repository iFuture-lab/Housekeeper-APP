from rest_framework import serializers
from .models import TempoararyDiscount,PromotionCode,CustomPackage


class CustomPackageSerializer(serializers.ModelSerializer):
    original_price = serializers.SerializerMethodField()
    discounted_price = serializers.SerializerMethodField()
    discount_applied = serializers.SerializerMethodField()
    class Meta:
        model = CustomPackage
        fields = '__all__'
        
    def get_original_price(self, obj):
        # Original price is the final price before applying any discount
        return obj.final_price

    def get_discount_applied(self, obj):
        # Return whether a discount is applied
        return obj.is_discount

    def get_discounted_price(self, obj):
        # Calculate the discounted price if a discount is applied
        if obj.is_discount and obj.temporary_discount:
            # Assuming temporary_discount.discount_amount is the discount amount
            discount_amount = (obj.temporary_discount.discount_percentage / 100) * obj.final_price
            return obj.final_price - discount_amount
        return obj.final_price
        
    
        
        

class DiscountSerializer(serializers.ModelSerializer):
    price_per_nationality = serializers.UUIDField() 
    class Meta:
        model = TempoararyDiscount
        fields = '__all__'
        
        
class PromotionCodeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PromotionCode
        fields = '__all__'