"""
Views for the equipment APIs
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Equipment
from equipment import serializers


class EquipmentViewSet(viewsets.ModelViewSet):
    """View for managing equipment APIs."""
    serializer_class = serializers.EquipmentSerializer
    queryset = Equipment.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve equipments for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')