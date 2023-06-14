"""
Views for the sample APIs
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Sample
from sample import serializers


class SampleViewSet(viewsets.ModelViewSet):
    """View for managing samples APIs."""
    serializer_class = serializers.SampleSerializer
    queryset = Sample.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve samples for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')