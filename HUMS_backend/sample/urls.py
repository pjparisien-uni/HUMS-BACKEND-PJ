"""
URL mappings for the equipment app.
"""
from django.urls import (path, include, )

from rest_framework.routers import DefaultRouter

from sample import views

router = DefaultRouter()
router.register('sample', views.SampleViewSet)

app_name = 'sample'

urlpatterns = [
    path('', include(router.urls)),
]
