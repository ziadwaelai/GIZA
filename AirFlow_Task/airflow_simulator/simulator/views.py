from django.shortcuts import render

# Create your views here.
import random
from django.http import JsonResponse

def kpi_endpoint(request):
    """Endpoint to calculate KPI."""
    value = float(request.GET.get('value', 0))
    result = value * random.uniform(1.0, 2.0)  # Example calculation
    return JsonResponse({'kpi': result})
