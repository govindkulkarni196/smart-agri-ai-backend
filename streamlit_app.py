import streamlit as st
import pickle
import pandas as pd

from weather_service import get_weather
from recommendation_engine import generate_recommendation

# ==========================================
# LOAD MODEL FILES
# ==========================================

model = pickle.load(open('risk_model.pkl', 'rb'))

scaler = pickle.load(open('scaler.pkl', 'rb'))

le_crop = pickle.load(open('crop_encoder.pkl', 'rb'))
le_season = pickle.load(open('season_encoder.pkl', 'rb'))
le_state = pickle.load(open('state_encoder.pkl', 'rb'))
le_risk = pickle.load(open('risk_encoder.pkl', 'rb'))

# ==========================================
# PAGE SETTINGS
# ==========================================

st.set_page_config(
    page_title="Smart Agricultural AI System",
    layout="centered"
)

st.title("🌾 Smart Agricultural Advisory System")

st.write("AI-powered crop yield risk prediction")

# ==========================================
# INPUTS
# ==========================================

crop = st.selectbox(
    "Select Crop",
    le_crop.classes_
)

season = st.selectbox(
    "Select Season",
    le_season.classes_
)

state = st.selectbox(
    "Select State",
    le_state.classes_
)

area = st.number_input(
    "Area",
    min_value=1.0
)

rainfall = st.number_input(
    "Annual Rainfall",
    min_value=0.0
)

fertilizer = st.number_input(
    "Fertilizer",
    min_value=0.0
)

pesticide = st.number_input(
    "Pesticide",
    min_value=0.0
)

lat = st.number_input(
    "Latitude",
    value=12.9716
)

lon = st.number_input(
    "Longitude",
    value=77.5946
)

# ==========================================
# PREDICT BUTTON
# ==========================================

if st.button("Predict Risk"):

    try:

        # WEATHER
        weather_data = get_weather(lat, lon)

        # ENCODE INPUTS
        crop_encoded = le_crop.transform([crop])[0]

        season_encoded = le_season.transform([season])[0]

        state_encoded = le_state.transform([state])[0]

        # CREATE DATAFRAME
        sample = pd.DataFrame([{

            'Crop': crop_encoded,

            'Season': season_encoded,

            'State': state_encoded,

            'Area': area,

            'Annual_Rainfall': rainfall,

            'Fertilizer': fertilizer,

            'Pesticide': pesticide

        }])

        # SCALE DATA
        sample_scaled = scaler.transform(sample)

        # PREDICT
        prediction = model.predict(sample_scaled)

        probabilities = model.predict_proba(sample_scaled)

        risk = le_risk.inverse_transform(prediction)[0]

        confidence = round(max(probabilities[0]) * 100, 2)

        # AI RECOMMENDATION
        recommendation = generate_recommendation(
            crop,
            risk,
            weather_data
        )

        # RESULTS
        st.subheader("📊 Prediction Result")

        st.success(f"Predicted Yield Risk: {risk}")

        st.info(f"Confidence: {confidence}%")

        st.subheader("🌦 Weather Information")

        st.write(weather_data)

        st.subheader("🤖 AI Recommendation")

        st.write(recommendation)

    except Exception as e:

        st.error(str(e))