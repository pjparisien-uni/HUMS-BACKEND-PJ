"""
Tests for sensor APIs.
"""
import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Sensor, Equipment

from sensor.serializers import (SensorSerializer,
                                SensorDetailSerializer,
                                )

SENSOR_URL = reverse('sensor:sensor-list')


def create_sensor(user, equipment, **params):
    """Create and return a sample equipment."""
    defaults = {
        'name': 'MS3505',
        'type': 'ODM',
        'serialNumber': '123456',
        'status': 0,
        'dateCreated': datetime.date.today(),
        'alarm': 0,

    }
    defaults.update(params)

    sensor = Sensor.objects.create(user=user, equipment=equipment, **defaults)
    return sensor


class PublicSensorAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(SENSOR_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateSensorAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='testpass123',
            organization='Gastops',
        )
        self.client.force_authenticate(self.user)
        self.equipment = Equipment.objects.create(
            user=self.user,
            name='sample Equipment',
            type='sample type',
        )

    def test_retrieve_sensors(self):
        """Test retrieving a list of equipments."""
        create_sensor(user=self.user, equipment=self.equipment)
        create_sensor(user=self.user, equipment=self.equipment)

        res = self.client.get(SENSOR_URL)

        sensors = Sensor.objects.all().order_by('-id')
        serializer = SensorSerializer(sensors, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_sensor_list_limited_to_user(self):
        """Test list of equipments is limited to authenticated user."""
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'password123',
        )
        create_sensor(user=other_user)
        create_sensor(user=self.user)

        res = self.client.get(SENSOR_URL)

        sensors = Sensor.objects.filter(user=self.user)
        serializer = SensorSerializer(sensors, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

