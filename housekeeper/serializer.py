from rest_framework import serializers
from .models import Housekeeper, HireRequest, RecruitmentRequest, TransferRequest,Status,HousekeeperRequestType
from login.models import CustomUser
from nationality.views import NationalitySerializer
from nationality.models import Nationallity
from .models import ActionLog
from django.utils import timezone
from decimal import Decimal
from service_type.models import ServiceType

from login.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'






    
    
    

class ActionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActionLog
        fields = '__all__'


#######################Status##################################

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'Status']




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
    # nationality = serializers.PrimaryKeyRelatedField(queryset=Nationallity.objects.all())
    salary = serializers.SerializerMethodField()
   
    request_types = serializers.PrimaryKeyRelatedField(
        queryset=ServiceType.objects.all(),
        many=True
    )
  
    class Meta:
        model = Housekeeper
        fields = '__all__'
        
    def get_salary(self, obj):
        custom_package = self.context.get('custom_package')
        if custom_package:
            print("hhhhhhhhhhhhhhhhhhhhhhhhhh")
            if obj.worked_before:
                print("jennnnnnnnnnnnnnnnnn")
                return custom_package.worked_before_salary
            else:
                print("hhhhhhhhhhhhhhhh")
                return custom_package.new_housekeeper_salary
       
        return 0
    
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('deleted_at', None)
        representation.pop('rating', None)
        
        
    
        return representation
        
        
    

        
        
    def create(self, validated_data):
        request_type_ids = validated_data.pop('request_types')
        housekeeper = Housekeeper.objects.create(**validated_data)
        housekeeper.request_types.set(request_type_ids)
        return housekeeper
    
    
    def update(self, instance, validated_data):
        request_type_ids = validated_data.pop('request_types', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if request_type_ids is not None:
            instance.request_types.set(request_type_ids)
        return instance

    
       
        
        
    

class HireRequestSerializer(serializers.ModelSerializer):
    
    # requester = serializers.UUIDField(read_only=True)
    # requester = CustomUserSerializer(read_only=True)
    
    # old_price = serializers.SerializerMethodField()
    # new_price = serializers.SerializerMethodField()
    # has_discount = serializers.SerializerMethodField()
    
    class Meta:
        model = HireRequest
        fields = '__all__'
        read_only_fields = ('requester',)
        
        
    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['requester'] = request.user
        else:
            raise serializers.ValidationError("Requester information is missing.")
        return super().create(validated_data)
    
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('deleted_at', None)
        representation.pop('temporary_discount', None)
    
        return representation
        
        
    # def get_old_price(self, obj):
    #     # Return the original price without any discounts
    #     return float(obj.total_price)

    # def get_new_price(self, obj):
    #     # Calculate the discounted price if applicable
    #     if obj.temporary_discount and obj.temporary_discount.is_active:
    #         now = timezone.now()
    #         if obj.temporary_discount.start_date <= now <= obj.temporary_discount.end_date:
    #             discount = Decimal(obj.temporary_discount.discount_percentage)  
    #             total_price = Decimal(obj.total_price)
    #             discount_amount = (total_price * discount) / Decimal(100) 
    #             total_price= float(total_price - discount_amount) 
    #             return total_price
    #     return float(Decimal(obj.total_price))  
            

    # def get_has_discount(self, obj):
    #     # Determine if a discount is active
    #     if obj.temporary_discount and obj.temporary_discount.is_active:
    #         print("""""""""""",obj.temporary_discount)
    #         now = timezone.now()
    #         if obj.temporary_discount.start_date <= now <= obj.temporary_discount.end_date:
    #             return True
    #     return False
    
    
    # def validate(self, data):
    #     # Automatically set is_discount to True if temporary_discount is provided
    #     if data.get('temporary_discount') is not None:
    #         data['is_discount'] = True
    #     else:
    #         data['is_discount'] = False
    #     return data
        
    

class RecruitmentRequestSerializer(serializers.ModelSerializer):
    # status = StatusSerializer()
    # old_price = serializers.SerializerMethodField()
    # new_price = serializers.SerializerMethodField()
    # has_discount = serializers.SerializerMethodField()
    # requester = serializers.UUIDField(read_only=True)
    # requester = CustomUserSerializer(read_only=True)
    class Meta:
        model = RecruitmentRequest
        fields = '__all__'
        read_only_fields = ('requester',)
        
        
    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['requester'] = request.user
        else:
            raise serializers.ValidationError("Requester information is missing.")
        return super().create(validated_data)
    
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('deleted_at', None)
        representation.pop('temporary_discount', None)
    
        return representation
        
    # def get_old_price(self, obj):
    #     # Return the original price without any discounts
    #     return float(obj.total_price)

    # def get_new_price(self, obj):
    #     # Calculate the discounted price if applicable
    #     if obj.temporary_discount and obj.temporary_discount.is_active:
    #         now = timezone.now()
    #         if obj.temporary_discount.start_date <= now <= obj.temporary_discount.end_date:
    #             discount = Decimal(obj.temporary_discount.discount_percentage)  
    #             total_price = Decimal(obj.total_price)
    #             discount_amount = (total_price * discount) / Decimal(100) 
    #             total_price= float(total_price - discount_amount) 
    #             return total_price
    #     return float(Decimal(obj.total_price))  
            

    # def get_has_discount(self, obj):
    #     # Determine if a discount is active
    #     if obj.temporary_discount and obj.temporary_discount.is_active:
    #         print("""""""""""",obj.temporary_discount)
    #         now = timezone.now()
    #         if obj.temporary_discount.start_date <= now <= obj.temporary_discount.end_date:
    #             return True
    #     return False
        
    

class TransferRequestSerializer(serializers.ModelSerializer):
    #requester = CustomUserSerializer(read_only=True)
    # requester = serializers.UUIDField(read_only=True)
    # old_price = serializers.SerializerMethodField()
    # new_price = serializers.SerializerMethodField()
    # has_discount = serializers.SerializerMethodField()
    # status = StatusSerializer()
    class Meta:
        model = TransferRequest
        fields = '__all__'
        read_only_fields = ('requester',)
        
        
    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['requester'] = request.user
        else:
            raise serializers.ValidationError("Requester information is missing.")
        return super().create(validated_data)
    
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('deleted_at', None)
        representation.pop('temporary_discount', None)
    
        return representation
        
    # def get_old_price(self, obj):
    #     # Return the original price without any discounts
    #     return float(obj.total_price)

    # def get_new_price(self, obj):
    #     # Calculate the discounted price if applicable
    #     if obj.temporary_discount and obj.temporary_discount.is_active:
    #         now = timezone.now()
    #         if obj.temporary_discount.start_date <= now <= obj.temporary_discount.end_date:
    #             discount = Decimal(obj.temporary_discount.discount_percentage)  
    #             total_price = Decimal(obj.total_price)
    #             discount_amount = (total_price * discount) / Decimal(100) 
    #             total_price= float(total_price - discount_amount) 
    #             return total_price
    #     return float(Decimal(obj.total_price))  
            

    # def get_has_discount(self, obj):
    #     # Determine if a discount is active
    #     if obj.temporary_discount and obj.temporary_discount.is_active:
    #         print("""""""""""",obj.temporary_discount)
    #         now = timezone.now()
    #         if obj.temporary_discount.start_date <= now <= obj.temporary_discount.end_date:
    #             return True
    #     return False
        
class HousekeeperIDSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    
    
class CombinedRequestsSerializer(serializers.Serializer):
   
    requests = serializers.DictField(child=serializers.ListSerializer(child=serializers.DictField()))
    # hire_requests = serializers.ListSerializer(child=HireRequestSerializer())
    # recruitment_requests = serializers.ListSerializer(child=RecruitmentRequestSerializer())
    # transfer_requests = serializers.ListSerializer(child=TransferRequestSerializer())
