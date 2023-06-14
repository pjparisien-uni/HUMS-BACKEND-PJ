"""
Serializers for the sample API View.
"""

from rest_framework import serializers

from core.models import Sample


class SampleSerializer(serializers.ModelSerializer):
    """Serializer for the sample object."""

    class Meta:
        model = Sample
        fields = '__all__'
        read_only_fields = ['id', 'date', 'time']


    def create(self, validated_data):
        sample = Sample.objects.create(
            sensor=validated_data['sensor'],
            sampleType=validated_data['sampleType'],
            valueType=validated_data['valueType'],
            value=validated_data['value']
        )
        return sample
    # def create(self, validated_data):
    #     """Create a sample"""
    #     samples_data = validated_data.pop('samples')
    #     sample = Sample.objects.create(**validated_data)
    #     for sample_data in samples_data:
    #         sample = Sample.objects.create(**sample_data)
    #         sample.sensors.add(sample)
    #     return sample

    def update(self, instance, validated_data):
        """Update a sample"""
        samples_data = validated_data.pop('samples')
        instance.sensor = validated_data.get('sensor', instance.sensor)
        instance.sampleType = validated_data.get('sampleType', instance.sampleType)
        instance.valueType = validated_data.get('valueType', instance.valueType)
        instance.value = validated_data.get('value', instance.value)
        instance.save()
        # for sensor_data in sensors_data:
        #     sensor, created = Sensor.objects.update_or_create(
        #         id=sensor_data.get('id', None),
        #         defaults=sensor_data
        #     )
        #     if created:
        #         instance.sensors.add(sensor)
        return instance