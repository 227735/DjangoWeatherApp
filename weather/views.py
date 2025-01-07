# 566533d279e0c79ffa5563c04a6606ad

import requests
from django.shortcuts import render
from datetime import datetime

def weather_view(request):
    city = request.GET.get('city', '')  # Domyślnie miasto puste, aby użytkownik mógł wpisać
    error = ''
    weather = None
    forecast = []
    show_input = True
    show_forecast = False
    sunrise = sunset = "Brak danych"  # Domyślna wartość, gdy brak danych

    if city:
        # Pobranie danych o pogodzie
        api_key = '3a263a1946ead7451ac6fcc415dd80ae'  # Wprowadź swój klucz API OpenWeatherMap
        weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=pl'

        try:
            response = requests.get(weather_url)
            data = response.json()

            if response.status_code == 200 and 'main' in data:
                weather = data
                lat = data['coord']['lat']
                lon = data['coord']['lon']
                # Pobranie prognozy
                forecast_url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric&lang=pl'
                forecast_response = requests.get(forecast_url)
                forecast_data = forecast_response.json()

                if forecast_response.status_code == 200 and 'list' in forecast_data:
                    forecast = forecast_data['list']
                    if 'show_forecast' in request.GET and request.GET['show_forecast'] == 'true':
                        show_forecast = True

                # Wschód i zachód słońca (sprawdzamy, czy są dostępne w danych)
                if 'sys' in data and 'sunrise' in data['sys'] and 'sunset' in data['sys']:
                    sunrise = datetime.utcfromtimestamp(data['sys']['sunrise']).strftime('%H:%M')
                    sunset = datetime.utcfromtimestamp(data['sys']['sunset']).strftime('%H:%M')
                else:
                    sunrise = sunset = "Brak danych"

                show_input = False
            else:
                error = 'Miasto nie zostało znalezione lub wystąpił błąd.'

        except Exception as e:
            error = f'Błąd połączenia z API: {str(e)}'

    context = {
        'city': city,
        'weather': weather,
        'forecast': forecast,
        'error': error,
        'show_input': show_input,
        'show_forecast': show_forecast,
        'sunrise': sunrise,
        'sunset': sunset,
    }
    return render(request, 'weather/weather.html', context)
