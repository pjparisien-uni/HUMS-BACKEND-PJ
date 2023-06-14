"""
URL mappings for the sensor app.
"""
from django.urls import (path, include,)

from rest_framework.routers import DefaultRouter

from sensor import views


router = DefaultRouter()
router.register('sensor', views.SensorViewSet)

app_name = 'sensor'

urlpatterns = [
    path('', include(router.urls)),
]