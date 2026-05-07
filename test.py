import requests

# Flask API URL
url = "http://127.0.0.1:5000/predict"

# Sample input data
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

# Send POST request
response = requests.post(url, json=sample_data)

# Print API response
print(response.json())