"""
Tests for equipment APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Equipment

from equipment.serializers import EquipmentSerializer

EQUIPMENT_URL = reverse('equipment:equipment-list')


def create_equipment(user, **params):
    """Create and return a sample equipment."""
    defaults = {
        'name': 'sample Equipment',
        'type': 'MS3505',
        'organization': 'Gastops',
    }
    defaults.update(params)

    equipment = Equipment.objects.create(user=user, **defaults)
    return equipment


class PublicEquipmentAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(EQUIPMENT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateEquipmentapiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='testpass123',
            organization='Gastops',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_equipments(self):
        """Test retrieving a list of equipments."""
        create_equipment(user=self.user)
        create_equipment(user=self.user)

        res = self.client.get(EQUIPMENT_URL)

        equipments = Equipment.objects.all().order_by('-id')
        serializer = EquipmentSerializer(equipments, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_equipment_list_limited_to_user(self):
        """Test list of equipments is limited to authenticated user."""
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'password123',
        )
        create_equipment(user=other_user)
        create_equipment(user=self.user)

        res = self.client.get(EQUIPMENT_URL)

        equipments = Equipment.objects.filter(user=self.user)
        serializer = EquipmentSerializer(equipments, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)