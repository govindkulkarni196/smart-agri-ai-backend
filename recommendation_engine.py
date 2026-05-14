from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

# ==========================================
# CONFIGURE GROQ CLIENT
# ==========================================

client = Groq(

    api_key=os.getenv("GROQ_API_KEY")

)

# ==========================================
# GENERATE AI RECOMMENDATION
# ==========================================

def generate_recommendation(crop, risk, risk_type, weather_data):

    temperature = weather_data["temperature"]

    humidity = weather_data["humidity"]

    rainfall = weather_data["current_rainfall"]

    # ======================================
    # AI PROMPT
    # ======================================

    prompt = f"""
You are an agricultural advisory assistant helping farmers.

Crop: {crop}

Risk Type: {risk_type}

Risk Level: {risk}

Current weather conditions:
- Temperature: {temperature} °C
- Humidity: {humidity} %
- Rainfall: {rainfall} mm

Generate practical farming advice.

Important Rules:
- Use very simple English
- Advice should sound natural and human
- Avoid scientific or technical terms
- Avoid scientific jargon
- Keep advice realistic
- Maximum 2 short lines
- Give practical suggestions
- Advice should match the risk type
- Advice should be useful for real farmers
- Use suitable emojis
- Keep response farmer-friendly
"""

    # ======================================
    # GENERATE RESPONSE
    # ======================================

    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.3,

        max_tokens=80
    )

    # ======================================
    # RETURN RESPONSE
    # ======================================

    return response.choices[0].message.content