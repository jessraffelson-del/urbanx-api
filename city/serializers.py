from rest_framework import serializers
from core.serializers import BulkCreateModelSerializer
from .models import CityService

class CityServiceSerializer(BulkCreateModelSerializer):
    class Meta:
        model = CityService
        fields = '__all__'
