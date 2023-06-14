"""
Views for the sensor APIs
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Sensor
from sensor import serializers


class SensorViewSet(viewsets.ModelViewSet):
    """View for managing equipment APIs."""
    serializer_class = serializers.SensorSerializer
    queryset = Sensor.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve equipments for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')