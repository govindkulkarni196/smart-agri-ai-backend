def calculate_disease_risk(temp, humidity, rainfall, wind_speed=0):

    score = 0
    reasons = []

    # ==========================================
    # HUMIDITY RULES
    # ==========================================

    if humidity >= 95:
        score += 6
        reasons.append("Extremely high humidity favors fungal diseases")

    elif humidity >= 85:
        score += 5
        reasons.append("Very high humidity increases disease spread")

    elif humidity >= 75:
        score += 4

    elif humidity >= 65:
        score += 3

    elif humidity >= 55:
        score += 2

    # ==========================================
    # RAINFALL RULES
    # ==========================================

    if rainfall >= 350:
        score += 6
        reasons.append("Extreme rainfall creates severe disease conditions")

    elif rainfall >= 250:
        score += 5
        reasons.append("Heavy rainfall may spread fungal infection")

    elif rainfall >= 150:
        score += 4

    elif rainfall >= 80:
        score += 3

    elif rainfall >= 30:
        score += 2

    # ==========================================
    # TEMPERATURE RULES
    # ==========================================

    if 24 <= temp <= 32:
        score += 5
        reasons.append("Temperature highly suitable for fungal growth")

    elif 20 <= temp <= 35:
        score += 3

    elif temp > 36:
        score += 1

    # ==========================================
    # WIND RULES
    # ==========================================

    if wind_speed >= 15:
        score += 3
        reasons.append("Strong wind may spread disease spores")

    elif wind_speed >= 10:
        score += 2

    elif wind_speed >= 5:
        score += 1

    # ==========================================
    # COMBINED WEATHER RULES
    # ==========================================

    if humidity > 90 and rainfall > 200:
        score += 6
        reasons.append("Wet and humid climate strongly favors disease outbreaks")

    if humidity > 85 and temp > 28:
        score += 4
        reasons.append("Warm humid weather accelerates fungal spread")

    if rainfall > 180 and wind_speed > 10:
        score += 4
        reasons.append("Rain and wind together may spread infection")

    if humidity > 80 and rainfall > 120 and temp > 26:
        score += 5
        reasons.append("Ideal fungal disease environment detected")

    if rainfall > 250 and humidity > 90 and wind_speed > 8:
        score += 5
        reasons.append("Extreme environmental stress may increase disease spread")

    # ==========================================
    # FINAL RISK
    # ==========================================

    if score >= 28:
        risk = "High"

    elif score >= 16:
        risk = "Medium"

    else:
        risk = "Low"

    return {
        "risk": risk,
        "score": score,
        "reasons": reasons
    }