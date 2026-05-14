import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")


def get_weather(lat, lon):

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

    response = requests.get(url)

    data = response.json()

    temperature = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    city = data["name"]
    weather = data["weather"][0]["description"]
    wind_speed = data["wind"]["speed"]

    rainfall = 0

    if "rain" in data:
        rainfall = data["rain"].get("1h", 0)

    return {
        "city": city,
        "temperature": temperature,
        "humidity": humidity,
        "weather": weather,
        "wind_speed": wind_speed,
        "rainfall": rainfall
    }