import requests

url = "https://web-production-16886.up.railway.app/predict"
sample_data = {

    "Crop": "Rice",

    "Season": "Kharif",

    "State": "Karnataka",

    "Area": 100,

    "Fertilizer": 80,

    "Pesticide": 20,

    "lat": 12.9716,

    "lon": 77.5946
}

response = requests.post(url, json=sample_data)

print(response.json())