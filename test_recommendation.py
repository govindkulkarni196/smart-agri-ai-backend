from recommendation_engine import generate_recommendation

weather_data = {

    "temperature": 38,

    "humidity": 80,

    "rainfall": 2
}

result = generate_recommendation(

    crop="Rice",

    risk="High",

    weather_data=weather_data
)

print(result)