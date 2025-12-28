def calculate_risk(ai_result, flags):
    score = 0

    if ai_result == "scam":
        score += 60

    score += len(flags) * 15

    return min(score, 100)
