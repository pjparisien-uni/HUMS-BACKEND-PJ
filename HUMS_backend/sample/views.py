"""
Views for the sample APIs
"""
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from core.models import Sample
from .serializers import SampleSerializer

class SampleList(generics.ListCreateAPIView):
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class SampleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]