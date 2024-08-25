

from rest_framework import serializers

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Nationallity

import base64
from django.core.files.base import ContentFile
import uuid
from django.core.files.uploadedfile import InMemoryUploadedFile


class NationalitySerializer(serializers.ModelSerializer):
    # image = serializers.CharField(write_only=True, required=False) 
    image = serializers.SerializerMethodField()

    class Meta:
        model = Nationallity
        fields = ['id', 'Nationality', 'image']
        
        
        
    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None
    
    
    def validate_Nationality(self, value):
        # Convert the value to lowercase for case-insensitive checking
        value_lower = value.lower()
        # Check if a record with the same nationality (case-insensitive) already exists
        if Nationallity.objects.filter(Nationality__iexact=value_lower).exists():
            raise serializers.ValidationError("This nationality already exists.")
        return value
    

    def create(self, validated_data):
        image_data = self.context['request'].data.get('image')
        
        if isinstance(image_data, str) and 'base64,' in image_data:
            # Handle base64 string
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f'{uuid.uuid4()}.{ext}')
            validated_data['image'] = data
        elif isinstance(image_data, ContentFile) or isinstance(image_data, InMemoryUploadedFile):
            # Handle standard file upload, no need to do anything
            pass

        return super().create(validated_data)

    
    # def create(self, validated_data):
    #     base64_image = validated_data.pop('image', None)
    #     nationality = Nationallity.objects.create(**validated_data)
    #     if base64_image:
    #         nationality.save_image_from_base64(base64_image, nationality.Nationality)
    #         nationality.save()
    #     return nationality

    # def update(self, instance, validated_data):
    #     base64_image = validated_data.pop('image', None)
    #     instance = super().update(instance, validated_data)
    #     if base64_image:
    #         instance.save_image_from_base64(base64_image, instance.Nationality)
    #         instance.save()
    #     return instance
        
        
        
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation.pop('deleted_at', None)
        
        

