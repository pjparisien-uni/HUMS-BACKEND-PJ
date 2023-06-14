"""
URL mappings for the equipment app.
"""
from django.urls import (path, include, )

from rest_framework.routers import DefaultRouter

from equipment import views

router = DefaultRouter()
router.register('equipment', views.EquipmentViewSet)

app_name = 'equipment'

urlpatterns = [
    path('', include(router.urls)),
]
