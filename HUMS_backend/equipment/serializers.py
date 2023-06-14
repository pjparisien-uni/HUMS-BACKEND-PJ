"""
Serializers for the equipment API View.
"""

from rest_framework import serializers

from core.models import Equipment


class EquipmentSerializer(serializers.ModelSerializer):
    """Serializer for the equipment object."""

    class Meta:
        model = Equipment
        fields = '__all__'
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create a equipment"""
        sensors_data = validated_data.pop('sensors')
        equipment = Equipment.objects.create(**validated_data)
        for sensor_data in sensors_data:
            sensor = Sensor.objects.create(**sensor_data)
            equipment.sensors.add(sensor)
        return equipment

    def update(self, instance, validated_data):
        """Update aquipment"""
        sensors_data = validated_data.pop('sensors')
        instance.name = validated_data.get('name', instance.name)
        instance.type = validated_data.get('type', instance.type)
        instance.organization = validated_data.get('organization', instance.organization)
        instance.save()
        for sensor_data in sensors_data:
            sensor, created = Sensor.objects.update_or_create(
                id=sensor_data.get('id', None),
                defaults=sensor_data
            )
            if created:
                instance.sensors.add(sensor)
        return instance