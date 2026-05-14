def calculate_pest_risk(temp, humidity, rainfall, wind_speed=0):

    score = 0
    reasons = []

    # ==========================================
    # TEMPERATURE RULES
    # ==========================================

    if temp >= 40:
        score += 5
        reasons.append("Extreme heat may increase pest reproduction")

    elif temp >= 35:
        score += 4
        reasons.append("High temperature supports pest activity")

    elif temp >= 30:
        score += 3
        reasons.append("Warm climate favors pest survival")

    elif temp >= 25:
        score += 2

    elif temp >= 20:
        score += 1

    # ==========================================
    # HUMIDITY RULES
    # ==========================================

    if humidity >= 90:
        score += 5
        reasons.append("Very high humidity increases pest survival")

    elif humidity >= 80:
        score += 4
        reasons.append("High humidity favors pest growth")

    elif humidity >= 70:
        score += 3

    elif humidity >= 60:
        score += 2

    elif humidity >= 50:
        score += 1

    # ==========================================
    # RAINFALL RULES
    # ==========================================

    if rainfall >= 300:
        score += 5
        reasons.append("Heavy rainfall may trigger pest outbreaks")

    elif rainfall >= 200:
        score += 4
        reasons.append("Excess rainfall supports insect breeding")

    elif rainfall >= 120:
        score += 3

    elif rainfall >= 60:
        score += 2

    elif rainfall >= 20:
        score += 1

    # ==========================================
    # WIND RULES
    # ==========================================

    if wind_speed >= 15:
        score += 3
        reasons.append("Strong winds may spread insects rapidly")

    elif wind_speed >= 10:
        score += 2

    elif wind_speed >= 5:
        score += 1

    # ==========================================
    # COMBINED ENVIRONMENT RULES
    # ==========================================

    if temp > 32 and humidity > 80:
        score += 4
        reasons.append("Hot and humid climate strongly favors pests")

    if rainfall > 150 and humidity > 85:
        score += 4
        reasons.append("Wet environment increases pest population")

    if temp > 36 and rainfall < 20:
        score += 3
        reasons.append("Dry heat may trigger sucking pests")

    if humidity > 90 and wind_speed > 10:
        score += 3
        reasons.append("Humid windy weather may spread pests")

    if rainfall > 250 and temp > 30:
        score += 4
        reasons.append("Warm wet climate creates severe pest conditions")

    # ==========================================
    # FINAL RISK
    # ==========================================

    if score >= 24:
        risk = "High"

    elif score >= 14:
        risk = "Medium"

    else:
        risk = "Low"

    return {
        "risk": risk,
        "score": score,
        "reasons": reasons
    }