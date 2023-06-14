"""
Serializers for the sensor API View.
"""

from rest_framework import serializers

from core.models import Sensor


class SensorSerializer(serializers.ModelSerializer):
    """Serializer for the equipment object."""

    class Meta:
        model = Sensor
        fields = ['equipment','name', 'type', 'serialNumber', 'status', 'dateCreated', 'alarm']
        read_only_fields = ['id']

    # def create(self, validated_data):
    #     """Create a equipment"""
    #     name = validated_data.pop('name', [])
    #     type = validated_data.pop('type', [])
    #     organization = validated_data.pop('organization')
