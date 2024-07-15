import requests

API_KEY = 'b99e0365b2724d388a5195404242706'

def get_weather(city=None, lat=None, lon=None):
    if city:
        url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"
    elif lat and lon:
        url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={lat},{lon}"
    else:
        raise ValueError("City name or latitude and longitude must be provided")
    
    response = requests.get(url)
    return response.json()

def get_location():
    url = 'https://ipinfo.io/json'
    response = requests.get(url)
    return response.json()

