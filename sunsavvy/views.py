from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.gis.geoip2 import GeoIP2

# Create your views here.

def location(request):
    return render(request, 'location.html')

def home(request):
    if request.method == 'POST':
        # Retrieve latitude and longitude from POST request
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        # Example: Print latitude and longitude
        print("Latitude:", latitude)
        print("Longitude:", longitude)

        # Add your processing logic here...

        # Return a JSON response indicating success
    return render(request, 'home.html')
    


def cloth_style(request):
    return render(request, 'cloth_style.html')


def sunscreen_safety(request):
    return render(request, 'sunscreen_safety.html')


def uv_impact(request):
    return render(request, 'uv_impact.html')