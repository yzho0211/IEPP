from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from .models import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import requests
import json
from datetime import datetime
import io
import urllib, base64
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def location(request):
    return render(request, 'location.html')


def get_data(lat= '', long= ''):
    onecall_url = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={long}&APPID=083c292f7560e22deb2fc5c8835bd786'
    try:
        response = requests.get(onecall_url)
        if response.status_code == 200:
            # Parse response JSON
            uv_data = response.json()
            return uv_data
        else:
            print(f"Failed to retrieve UV index data from One Call API. {response.status_code}")
    except Exception as e:
        print(f"An error occurred while fetching data from the One Call API: {e}")

    
def login_view(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        user = authenticate(request, password=password)
        if user is not None:
            login(request, user)
            if request.user.is_authenticated:
                print("authenticated")
                return redirect('home')
            else:
                return render(request, 'login.html', {'error_message': 'Invalid password'})
    return render(request, 'login.html')

@login_required 
def home(request):
    if request.method == 'POST':
        # Check if the user is authenticated
        # if not request.session.get('authenticated'):
        #     return redirect('login')  # Redirect to login page if not authenticated

        # Retrieve latitude and longitude from POST request
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        print(latitude, longitude)
        # Store latitude and longitude in session
        request.session['latitude'] = latitude
        request.session['longitude'] = longitude
        print(latitude, longitude)

        # Redirect to the home page to avoid duplicate form submissions
        return redirect('home')

    # If it's a GET request, render the home page template
    return render(request, 'home.html')

# def home(request):
#     if request.method == 'POST':
#         # Retrieve latitude and longitude from POST request
        
#         latitude = request.POST.get('latitude')
#         longitude = request.POST.get('longitude')
#         # context = {"Latitude": latitude, "Longitude": longitude}
#         # Example: Print latitude and longitude
#         print("Latitude:", latitude)
#         print("Longitude:", longitude)

#         request.session['latitude'] = latitude
#         request.session['longitude'] = longitude
#     return render(request, 'home.html')
    


# def cloth_style(request):
#     latitude = request.session.get('latitude')
#     longitude = request.session.get('longitude')

#     data = get_data(latitude, longitude)
#     # hourly data
#     hourly_data = data['hourly']
#     uv_indices = [hour['uvi'] for hour in hourly_data[:24]]
#     uv_index = max(uv_indices)

#     return render(request, 'cloth_style.html', {"uv_index": uv_index})

@login_required
def sunscreen_safety(request):
    latitude = request.session.get('latitude')
    longitude = request.session.get('longitude')

    data = get_data(latitude, longitude)
    # hourly data
    hourly_data = data['hourly']
    uv_indices = [hour['uvi'] for hour in hourly_data[:24]]
    uv_index = max(uv_indices)
    # print(uv_index)
    return render(request, 'sunscreen_safety.html', {"uv_index": uv_index})

@login_required
def uv_impact(request):
    latitude = request.session.get('latitude')
    longitude = request.session.get('longitude')


    data = get_data(latitude, longitude)
    # hourly data
    hourly_data = data['hourly']
    #print(hourly_data)
    timestamps = [hour['dt'] for hour in hourly_data[:24]]
    uv_indices = [hour['uvi'] for hour in hourly_data[:24]]
    
    # Convert timestamps to datetime objects
    dates = [datetime.utcfromtimestamp(ts) for ts in timestamps]
    
    # # Extracting hours with AM/PM format
    hours = [date.strftime('%I %p') for date in dates]
    
    
    #Swap AM and PM labels (still unsure)
    for i in range(len(hours)):
        if hours[i].endswith('AM'):
            hours[i] = hours[i].replace('AM', 'PM')
        else:
            hours[i] = hours[i].replace('PM', 'AM')
    
    #Plotting UV index over time for the first 24 entries
    # plt.figure(figsize=(10, 6))
    plt.plot(hours, uv_indices, marker='o', linestyle='-')
    # Define UV index ranges and corresponding colors
    uv_ranges = [(0, 2), (2, 5), (5, 8), (8, 10), (10, 13)]
    uv_colors = ['green', 'yellow', 'orange', 'red', 'purple']
    
    # Fill between the curve and the bottom of the plot for each UV index range
    for uv_range, color in zip(uv_ranges, uv_colors):
        plt.fill_between(hours, uv_range[0], uv_range[1], color=color, alpha=0.3)
    plt.title(f'Hourly UV Index')
    plt.xlabel('Hour (AM/PM)')
    plt.xticks(rotation=45)
    plt.ylabel('UV Index')
    plt.grid(True)
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close()

    # Embed the plot in the HTML template
    graphic = urllib.parse.quote(base64.b64encode(image_png))
    return render(request, 'uv_impact.html', {'graphic': graphic})