"""
Database models.
"""
import uuid
import os
import datetime

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    organization = models.CharField(max_length=255, default='')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Equipment(models.Model):
    """Equipment object."""
    EQUIPMENT_TYPE_CHOICES = (
        ('V', 'Vehicle'),
        ('M', 'Marine'),
        ('A', 'Aerial'),
        ('S', 'Stationary'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )
    name = models.CharField(max_length=100,)
    type = models.CharField(max_length=1, choices=EQUIPMENT_TYPE_CHOICES)
    organization = models.CharField(max_length=100,)
    sensors = models.ManyToManyField('Sensor', related_name='equipment_sensors', blank=True)

    def __str__(self):
        return self.name


class Sensor(models.Model):
    """Sensor object."""
    SENSOR_TYPE_CHOICES = (
        ('O', 'Oil'),
        ('M', 'Metal'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )
    equipment = models.ForeignKey(Equipment, on_delete=models.PROTECT)
    name = models.CharField(blank=False, max_length=100)
    type = models.CharField(max_length=1, choices=SENSOR_TYPE_CHOICES)
    serialNumber = models.CharField(max_length=10, unique=True)
    status = models.IntegerField()
    dateCreated = models.DateField(default=datetime.date.today, editable=False)
    alarm = models.IntegerField()

    readonly_fields = ['dateCreated']

    def __str__(self):
        return self.name


class Sample(models.Model):
    """sample object."""
    SAMPLE_TYPE_CHOICES = (
        ('O', 'Oil'),
        ('M', 'Metal'),
    )

    SAMPLE_VALUE_CHOICES = (
        ('OW', 'Water'),
        ('OF', 'Fuel'),
        ('MF', 'Ferrous'),
        ('MN', 'Non-Ferrous'),
    )

    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='samples')
    sampleType = models.CharField(max_length=1, choices=SAMPLE_TYPE_CHOICES)
    valueType = models.CharField(max_length=2, choices=SAMPLE_VALUE_CHOICES)
    value = models.FloatField()
    date = models.DateField()
    time = models.TimeField()

    readonly_fields = ['date', 'time', ]

    def __str__(self):
        return str(self.value)


class Event(models.Model):
    """
    Event object
    Events refer to occurrences detected by a sensor, including status updates, failures, and other related phenomena.
    """
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='event')
    description = models.TextField()
    date_time = models.DateTimeField()

    def __str__(self):
        return f"{self.description} at {self.date_time}"


class MaintenanceSchedule(models.Model):
    """
    MaintenanceSchedule object
    """
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='maintenance_schedules')
    oil_sample_timeslot = models.PositiveIntegerField(help_text='Hours before next oil sample needed')
    lubrication_replacement = models.PositiveIntegerField(help_text='Hours before next lubrication replacement needed')
    engine_inspection = models.PositiveIntegerField(help_text='Hours before next engine inspection needed')
    maintenance_required = models.BooleanField(default=False)

    def __str__(self):
        return f"Maintenance Schedule for {self.equipment.name}"
