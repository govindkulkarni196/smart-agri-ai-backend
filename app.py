from flask import Flask, request, jsonify
import pickle
import pandas as pd

# IMPORT WEATHER SERVICE
from weather_service import get_weather

# IMPORT AI RECOMMENDATION ENGINE
from recommendation_engine import generate_recommendation

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

# ==========================================
# HOME ROUTE
# ==========================================

@app.route('/')
def home():

    return "Smart Agricultural Yield Risk Prediction API Running"

# ==========================================
# PREDICTION ROUTE
# ==========================================

@app.route('/predict', methods=['POST'])
def predict():

    try:

        # ==================================
        # GET JSON INPUT
        # ==================================

        data = request.get_json()

        # ==================================
        # GET LOCATION
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
        # ENCODE INPUTS
        # ==================================

        crop_encoded = le_crop.transform([data['Crop']])[0]

        season_encoded = le_season.transform([data['Season']])[0]

        state_encoded = le_state.transform([data['State']])[0]

        # ==================================
        # SAFE RAINFALL INPUT
        # ==================================

        annual_rainfall = float(data.get('Annual_Rainfall', 0))

        # ==================================
        # CREATE DATAFRAME
        # ==================================

        sample = pd.DataFrame([{

            'Crop': crop_encoded,

            'Season': season_encoded,

            'State': state_encoded,

            'Area': float(data['Area']),

            'Annual_Rainfall': annual_rainfall,

            'Fertilizer': float(data['Fertilizer']),

            'Pesticide': float(data['Pesticide'])

        }])

        # ==================================
        # SCALE INPUT
        # ==================================

        sample_scaled = scaler.transform(sample)

        # ==================================
        # PREDICT YIELD RISK
        # ==================================

        prediction = model.predict(sample_scaled)

        probabilities = model.predict_proba(sample_scaled)

        # Decode prediction
        risk = le_risk.inverse_transform(prediction)[0]

        # Confidence %
        confidence = round(max(probabilities[0]) * 100, 2)

        # ==================================
        # LIVE ENVIRONMENT DATA
        # ==================================

        live_environment = None

        if weather_data:

            live_environment = {

                "temperature": weather_data["temperature"],

                "humidity": weather_data["humidity"],

                "current_rainfall": weather_data["rainfall"]

            }

        # ==================================
        # AI RECOMMENDATION ENGINE
        # ==================================

        recommendation = "Weather data unavailable."

        if weather_data:

            recommendation = generate_recommendation(

                crop=data["Crop"],

                risk=risk,

                weather_data=weather_data
            )

        # ==================================
        # RETURN RESPONSE
        # ==================================

        return jsonify({

            "predicted_risk": risk,

            "confidence_percent": confidence,

            "class_probabilities": probabilities.tolist(),

            "weather": weather_data,

            "live_environment": live_environment,

            "recommendation": recommendation

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