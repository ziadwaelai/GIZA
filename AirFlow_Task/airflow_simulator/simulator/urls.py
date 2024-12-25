from django.urls import path
from . import views

urlpatterns = [
    path('kpi/', views.kpi_endpoint, name='kpi-endpoint'),
]
