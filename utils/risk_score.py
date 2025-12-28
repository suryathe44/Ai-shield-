def calculate_risk(ai_result, reasons):
    risk = 0

    # Rule-based weight
    if "money" in reasons:
        risk += 35
    if "urgency" in reasons:
        risk += 30
    if "bank" in reasons:
        risk += 25

    # AI model boost
    if ai_result == "scam":
        risk += 40

    # Cap risk
    return min(risk, 100)
