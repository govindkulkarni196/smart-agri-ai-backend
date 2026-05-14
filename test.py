import requests

url = "http://127.0.0.1:5000/predict"

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