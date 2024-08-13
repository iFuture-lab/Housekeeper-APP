from rest_framework import serializers
from .models import TempoararyDiscount,PromotionCode,CustomPackage
from django.utils import timezone
from decimal import Decimal
from nationality.models import Nationallity

        

class DiscountSerializer(serializers.ModelSerializer):
    price_per_nationality = serializers.UUIDField() 
    class Meta:
        model = TempoararyDiscount
        fields = '__all__'
        
        
class PromotionCodeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PromotionCode
        fields = '__all__'
        
        
class CustomPackageSerializer(serializers.ModelSerializer):
    old_price = serializers.SerializerMethodField()
    new_price = serializers.SerializerMethodField()
    has_discount = serializers.SerializerMethodField()
    
    nationallities = serializers.PrimaryKeyRelatedField(queryset=Nationallity.objects.all(), many=True)

    class Meta:
        model = CustomPackage
        fields = '__all__'

    def get_old_price(self, obj):
        # Return the original price without any discounts
        return float(obj.final_price)

    def get_new_price(self, obj):
        # Calculate the discounted price if applicable
        if obj.temporary_discount and obj.temporary_discount.is_active:
            now = timezone.now()
            if obj.temporary_discount.start_date <= now <= obj.temporary_discount.end_date:
                discount = Decimal(obj.temporary_discount.discount_percentage)  
                final_price = Decimal(obj.final_price)  
                discount_amount = (final_price * discount) / Decimal(100) 
                final_price= float(final_price - discount_amount) 
                return  final_price
        return float(Decimal(obj.final_price))  
            

    def get_has_discount(self, obj):
        # Determine if a discount is active
        if obj.temporary_discount and obj.temporary_discount.is_active:
            print("""""""""""",obj.temporary_discount)
            now = timezone.now()
            if obj.temporary_discount.start_date <= now <= obj.temporary_discount.end_date:
                return True
        return False
    
    
    def validate(self, data):
        # Automatically set is_discount to True if temporary_discount is provided
        if data.get('temporary_discount') is not None:
            data['is_discount'] = True
        else:
            data['is_discount'] = False
        return data
    
    def create(self, validated_data):
        nationallity_ids = validated_data.pop('nationallities')
        custom_package = CustomPackage.objects.create(**validated_data)
        custom_package.nationallities.set(nationallity_ids)  # Add nationalities to the custom_package
        return custom_package
    
    

    def update(self, instance, validated_data):
        nationallity_ids = validated_data.pop('nationallities', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if nationallity_ids is not None:
            instance.nationalities.set(nationallity_ids)
        return instance