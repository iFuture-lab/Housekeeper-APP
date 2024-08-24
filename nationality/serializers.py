

from rest_framework import serializers

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Nationallity


class NationalitySerializer(serializers.ModelSerializer):
    image = serializers.CharField(write_only=True, required=False)  # Base64 image field

    class Meta:
        model = Nationallity
        fields = ['id', 'Nationality', 'image']

    
    def create(self, validated_data):
        base64_image = validated_data.pop('image', None)
        nationality = Nationallity.objects.create(**validated_data)
        if base64_image:
            nationality.save_image_from_base64(base64_image, nationality.Nationality)
            nationality.save()
        return nationality

    def update(self, instance, validated_data):
        base64_image = validated_data.pop('image', None)
        instance = super().update(instance, validated_data)
        if base64_image:
            instance.save_image_from_base64(base64_image, instance.Nationality)
            instance.save()
        return instance
        
        
        
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation.pop('deleted_at', None)
        
        

