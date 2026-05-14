import requests

API_KEY = "3062b7e28b46b4b1b706240dd9d496e3"

lat = 12.9716
lon = 77.5946

url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

response = requests.get(url)

data = response.json()

# Extract weather values
temperature = data["main"]["temp"]
humidity = data["main"]["humidity"]
city = data["name"]
weather = data["weather"][0]["description"]
wind_speed = data["wind"]["speed"]

# Safe rainfall extraction
rainfall = 0

if "rain" in data:
    rainfall = data["rain"].get("1h", 0)

# Print results
print("City:", city)
print("Temperature:", temperature, "°C")
print("Humidity:", humidity, "%")
print("Weather:", weather)
print("Wind Speed:", wind_speed)
print("Rainfall (last 1 hour):", rainfall, "mm")