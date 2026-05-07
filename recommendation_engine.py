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

def generate_recommendation(crop, risk, weather_data):

    temperature = weather_data["temperature"]

    humidity = weather_data["humidity"]

    rainfall = weather_data["rainfall"]

    # ======================================
    # AI PROMPT
    # ======================================

    prompt = f"""
You are an agricultural advisory assistant helping farmers improve crop yield.

Crop: {crop}

Predicted yield risk: {risk}

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
- Avoid exact measurements unless necessary
- Focus on improving crop yield
- Maximum 5 short points
- Do not exaggerate
- Give practical yield-improvement suggestions
- Advice should be useful for real farmers
- Use suitable emojis to make it more engaging
- Recommend actions based on the risk level (e.g., if risk is high, recommend more protective measures)
- Advice should sound like a real agricultural advisory system
- Keep advice  realistic and actionable
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

        max_tokens=90
    )

    # ======================================
    # RETURN RESPONSE
    # ======================================

    return response.choices[0].message.content