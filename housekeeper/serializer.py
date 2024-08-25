from rest_framework import serializers
from .models import Housekeeper, HireRequest, RecruitmentRequest, TransferRequest,Status,HousekeeperRequestType
from login.models import CustomUser
from nationality.views import NationalitySerializer
from nationality.models import Nationallity
from .models import ActionLog,Religion,EmploymentType
from django.utils import timezone
from decimal import Decimal
from service_type.models import ServiceType

from login.models import CustomUser
from .religion_view import ReligionSerializer
from .employment_type_view import EmploymentTypeSerializer
from service_type.serializers import ServiceTypeSerializer
from .models import HousekeeperRequestType
from nationality.models import Nationallity





class HousekeeperRequestTypeSerializer(serializers.ModelSerializer):
    request_type = ServiceTypeSerializer()

    class Meta:
        model = HousekeeperRequestType
        fields = ['id', 'request_type']

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
        fields = ['id']  
        
class DummyHireHousekeeperSerializer(serializers.ModelSerializer):
    class Meta:
        model = HireRequest
        fields = ['id']  
        
class DummyTransferRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferRequest
        fields = ['id']  
        
class DummyRecruitmentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecruitmentRequest
        fields = ['id']  

class HousekeeperSerializer(serializers.ModelSerializer):
    # nationality = serializers.PrimaryKeyRelatedField(queryset=Nationallity.objects.all())
    
    # religion = ReligionSerializer()
    # employment_type = EmploymentTypeSerializer()
    # nationality = NationalitySerializer()
    
   
    # request_types = ServiceTypeSerializer(many=True)
    #requests_types = HousekeeperRequestTypeSerializer(source='housekeeperrequesttype_set', many=True)
    salary = serializers.SerializerMethodField()
    request_types_detail= serializers.SerializerMethodField()
    
    
   
    request_types = serializers.PrimaryKeyRelatedField(
        queryset=ServiceType.objects.all(),
        many=True
    )
    
    religion = serializers.PrimaryKeyRelatedField(
        queryset=Religion.objects.all(),
      
        write_only=True
    )
    employment_type = serializers.PrimaryKeyRelatedField(
        queryset=EmploymentType.objects.all(),
      
        write_only=True
    )
    nationality = serializers.PrimaryKeyRelatedField(
        queryset=Nationallity.objects.all(),
        write_only=True
    )
    
   
    religion_detail = serializers.SerializerMethodField()
    employment_type_detail = serializers.SerializerMethodField()
    nationality_detail = serializers.SerializerMethodField()

    class Meta:
        model = Housekeeper
        fields = '__all__'  # or specify the fields you want to include
        extra_kwargs = {
            'religion': {'write_only': True},
            'employment_type': {'write_only': True},
            'nationality': {'write_only': True},
        }

    def get_religion_detail(self, obj):
        return ReligionSerializer(obj.religion).data

    def get_employment_type_detail(self, obj):
        return EmploymentTypeSerializer(obj.employment_type).data

    def get_nationality_detail(self, obj):
        return NationalitySerializer(obj.nationality).data
    
    def get_request_types_detail(self, obj):
        return ServiceTypeSerializer(obj.request_types.all(), many=True).data
  
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
    employment_type = serializers.SerializerMethodField()
   
    housekeeper_detail = serializers.SerializerMethodField()
    status_detail = serializers.SerializerMethodField()
    
    
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
    
    def get_housekeeper_detail(self, obj):
        return HousekeeperSerializer(obj.housekeeper).data

    def get_status_detail(self, obj):
        return StatusSerializer(obj.status).data
    
    def get_employment_type(self, obj):
        return obj.housekeeper.employment_type.name if obj.housekeeper and obj.housekeeper.employment_type else None
    
      # housekeeper = HousekeeperSerializer()
    # request_type = ServiceTypeSerializer()
    # status=StatusSerializer()
    
   
    # housekeeper = serializers.PrimaryKeyRelatedField(
    #     queryset=Housekeeper.objects.all(),    
    #     write_only=True
    # )
    
    # status = serializers.PrimaryKeyRelatedField(
    #     queryset=Status.objects.all(),
    #     write_only=True
    # )
        
        
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
    employment_type = serializers.SerializerMethodField()
    housekeeper_detail = serializers.SerializerMethodField()
    status_detail = serializers.SerializerMethodField()
    # housekeeper = HousekeeperSerializer()
    # request_type = ServiceTypeSerializer()
    # status=StatusSerializer()
    
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
    
    
    def get_housekeeper_detail(self, obj):
        return HousekeeperSerializer(obj.housekeeper).data

    def get_status_detail(self, obj):
        return StatusSerializer(obj.status).data
    
    
    def get_employment_type(self, obj):
        return obj.housekeeper.employment_type.name if obj.housekeeper and obj.housekeeper.employment_type else None
        
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
    
    # housekeeper = HousekeeperSerializer()
    # request_type = ServiceTypeSerializer()
    # status=StatusSerializer()
    
    employment_type = serializers.SerializerMethodField()
    housekeeper_detail = serializers.SerializerMethodField()
    status_detail = serializers.SerializerMethodField()
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
    
    
    
    def get_housekeeper_detail(self, obj):
        return HousekeeperSerializer(obj.housekeeper).data

    def get_status_detail(self, obj):
        return StatusSerializer(obj.status).data
    
    
    def get_employment_type(self, obj):
        return obj.housekeeper.employment_type.name if obj.housekeeper and obj.housekeeper.employment_type else None
        
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
