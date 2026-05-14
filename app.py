from flask import Flask, request, jsonify
import pickle
import pandas as pd
from flask_cors import CORS
# WEATHER SERVICE
from weather_utils import get_weather

# RECOMMENDATION ENGINE
from recommendation_engine import generate_recommendation

# RULE ENGINES
from pest_rules import calculate_pest_risk
from disease_rules import calculate_disease_risk

# ==========================================
# LOAD SAVED FILES
# ==========================================

model = pickle.load(open('risk_model.pkl', 'rb'))

scaler = pickle.load(open('scaler.pkl', 'rb'))

le_crop = pickle.load(open('crop_encoder.pkl', 'rb'))
le_season = pickle.load(open('season_encoder.pkl', 'rb'))
le_state = pickle.load(open('state_encoder.pkl', 'rb'))
le_risk = pickle.load(open('risk_encoder.pkl', 'rb'))

# ==========================================
# CREATE FLASK APP
# ==========================================

app = Flask(__name__)
CORS(app)

# ==========================================
# HOME ROUTE
# ==========================================

@app.route('/')
def home():

    return "Smart Agriculture AI Backend Running"

# ==========================================
# PREDICTION ROUTE
# ==========================================

@app.route('/predict', methods=['POST'])
def predict():

    try:

        # ==================================
        # GET INPUT DATA
        # ==================================

        data = request.get_json()

        # ==================================
        # GPS LOCATION
        # ==================================

        lat = data.get("lat")
        lon = data.get("lon")

        # ==================================
        # FETCH LIVE WEATHER
        # ==================================

        weather_data = None

        if lat is not None and lon is not None:

            weather_data = get_weather(lat, lon)

        # ==================================
        # WEATHER VALUES
        # ==================================

        temperature = 30
        humidity = 60
        rainfall = 0
        wind_speed = 0

        if weather_data:

            temperature = weather_data["temperature"]

            humidity = weather_data["humidity"]

            rainfall = weather_data["rainfall"]

            wind_speed = weather_data.get("wind_speed", 0)

        # ==================================
        # ENCODE INPUTS
        # ==================================

        crop_encoded = le_crop.transform([data['Crop']])[0]

        season_encoded = le_season.transform([data['Season']])[0]

        state_encoded = le_state.transform([data['State']])[0]

        # ==================================
        # CREATE DATAFRAME
        # ==================================

        sample = pd.DataFrame([{

            'Crop': crop_encoded,

            'Season': season_encoded,

            'State': state_encoded,

            'Area': float(data['Area']),

            'Annual_Rainfall': rainfall,

            'Fertilizer': float(data['Fertilizer']),

            'Pesticide': float(data['Pesticide'])

        }])

        # ==================================
        # SCALE INPUT
        # ==================================

        sample_scaled = scaler.transform(sample)

        # ==================================
        # YIELD RISK PREDICTION
        # ==================================

        prediction = model.predict(sample_scaled)

        probabilities = model.predict_proba(sample_scaled)

        yield_risk = le_risk.inverse_transform(prediction)[0]

        confidence = round(max(probabilities[0]) * 100, 2)

        # ==================================
        # PEST RISK
        # ==================================

        pest_result = calculate_pest_risk(

            temperature,
            humidity,
            rainfall,
            wind_speed

        )

        pest_risk = pest_result["risk"]

        # ==================================
        # DISEASE RISK
        # ==================================

        disease_result = calculate_disease_risk(

            temperature,
            humidity,
            rainfall,
            wind_speed

        )

        disease_risk = disease_result["risk"]

        # ==================================
        # LIVE ENVIRONMENT
        # ==================================

        live_environment = {

            "temperature": temperature,

            "humidity": humidity,

            "current_rainfall": rainfall,

            "wind_speed": wind_speed

        }

        # ==================================
        # AI SUGGESTIONS
        # ==================================

        yield_suggestion = generate_recommendation(

            crop=data["Crop"],

            risk=yield_risk,

            risk_type="Yield Risk",

            weather_data=live_environment

        )

        pest_suggestion = generate_recommendation(

            crop=data["Crop"],

            risk=pest_risk,

            risk_type="Pest Risk",

            weather_data=live_environment

        )

        disease_suggestion = generate_recommendation(

            crop=data["Crop"],

            risk=disease_risk,

            risk_type="Disease Risk",

            weather_data=live_environment

        )

        # ==================================
        # RETURN RESPONSE
        # ==================================

        return jsonify({

            "yield_risk": yield_risk,

            "pest_risk": pest_risk,

            "disease_risk": disease_risk,

            "confidence_percent": confidence,

            "class_probabilities": probabilities.tolist(),

            "weather": weather_data,

            "live_environment": live_environment,

            "pest_details": pest_result,

            "disease_details": disease_result,

            "yield_suggestion": yield_suggestion,

            "pest_suggestion": pest_suggestion,

            "disease_suggestion": disease_suggestion

        })

    except Exception as e:

        return jsonify({

            "error": str(e)

        })

# ==========================================
# RUN SERVER
# ==========================================

if __name__ == '__main__':

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )