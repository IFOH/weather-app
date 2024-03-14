from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from . models import *
import requests

#Map weather conditions to weather icons
def get_icon_filename(conditions):
    condition_icons = {
        'rain': 'rain.png',
        'drizzle': 'rain.png',
        'clear': 'clear-day.png',
        'sunshine': 'clear-day.png',
        'fog': 'fog.png',
        'partially cloudy': 'cloudy.png',
        'overcast': 'cloudy.png',
        'hail': 'hail.png',
        'thunderstorm': 'thunder-rain.png',
        'ice': 'sleet.png',
        'windy': 'wind.png',
    }
    return condition_icons.get(conditions.lower(), 'clear-day.png') #Clean "conditions" string using lower(). 
                                                                    #Return 'clear-day.png' by default 

def home(request):

    context = {"places": []}
    queries = {
        'aggregateHours': '24',
        'contentType': 'json',
        'unitGroup': 'metric',
        'locationMode': 'single',
        'key': 'BP8GPRYV53UQ56SHJR5EFCJ77',
        'locations': ''
    }

    #When user searches for a place
    if request.method == 'GET':
        place_name = request.GET.get('place_name')
        if place_name: #If place_name query is in request, attempt an api request to check for valid api request
            queries['locations'] = place_name
            response = requests.get("https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/forecast", params=queries)
            
            if response.status_code == 200: #Valid api response
                Place.objects.create(name=place_name)
                messages.success(request, "City added successfully!")
            elif Place.objects.filter(name__iexact=place_name).exists():
                messages.error(request, "City already exists in the list!")
            else:
                messages.error(request, ("City '%s' does not exist in the world!" %place_name)) #Format message to include place name
            return redirect('home')

    #Make queries for each location in the database
    for p in Place.objects.all():
        queries['locations'] = p.name
        response = requests.get("https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/forecast", params=queries)
        
        if response.status_code == 200: #Valid api response
            data = response.json()
            conditions = data['location']['values'][0]['conditions']
            context['places'].append({
                'name': p.name,
                'temperature': data['location']['currentConditions']['temp'],
                'conditions': conditions,
                'icon_filename': get_icon_filename(conditions.split(',')[0].strip()) #Take the first condition if there are multiple
            })

    return render(request, 'weather_page/home_view.html',context)

def delete(request, place_name):
    place = get_object_or_404(Place, name=place_name)
    place.delete()
    messages.success(request, ("Successfully deleted %s" % place_name)) #Format message to include place name
    return redirect('home')