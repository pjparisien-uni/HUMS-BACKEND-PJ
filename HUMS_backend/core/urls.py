from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from core import views
from sample.views import SampleList, SampleDetail

urlpatterns = [
    path('samples/', views.SampleList.as_view()),
    path('samples/<int:pk>/', views.SampleDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)