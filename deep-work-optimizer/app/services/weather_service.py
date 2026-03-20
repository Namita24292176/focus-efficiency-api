import requests
import os

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

def get_weather(city):

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception:
        return {"main": {"temp": 15}}