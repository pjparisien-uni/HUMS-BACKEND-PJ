"""
Tests for models.
"""
import datetime
from unittest.mock import patch
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.timezone import timezone


from core import models


def create_user(email='user@example.com', password='testpass123'):
    """Create a return a new user."""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        organization = 'Gastops'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            organization=organization
        )

        self.assertEqual(user.email, email)
        self.assertEqual(user.organization, organization)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_equipment(self):
        """Test creating equipment is successful."""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
            organization='gastops',
        )
        equipment = models.Equipment.objects.create(
            user=user,
            name='sample Equipment',
            type='sample type',
        )

        self.assertEqual(str(equipment), equipment.name)

    def test_create_sensor(self):
        """Test creating sensor is successful."""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
            organization='gastops',
        )
        equipment= models.Equipment.objects.create(
            user=user,
            name='sample Equipment',
            type='sample type',
        )
        date = datetime.date
        sensor = models.Sensor.objects.create(
            user=user,
            equipment=equipment,
            name='sample Sensor name',
            type='sample Sensor type',
            serialNumber='123456',
            status=0,
            alarm=20,
        )

        self.assertEqual(str(sensor), sensor.name)