from django.shortcuts import render
from .models import Nationallity
from rest_framework import serializers

# Create your views here.
class NationalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Nationallity
        fields = ['id', 'Nationallity']