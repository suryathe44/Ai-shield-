from flask import Flask, render_template, request
import joblib
import os

from utils.rules import rule_based_check
from utils.risk_score import calculate_risk

app = Flask(__name__)

# ---------------- LOAD MODEL SAFELY ----------------
model = None
vectorizer = None

try:
    model = joblib.load("model/scam_model.pkl")
    vectorizer = joblib.load("model/vectorizer.pkl")
    print("✅ ML model loaded")
except Exception as e:
    print("⚠️ ML model not loaded, rule-based mode only")
    print(e)

# ---------------- AI PREDICTION ----------------
def ai_predict(text):
    if model is None or vectorizer is None:
        return "unknown"
    text_vec = vectorizer.transform([text])
    return model.predict(text_vec)[0]

# ---------------- ROUTE ----------------
@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    risk = 0
    reasons = []

    if request.method == "POST":
        text = request.form.get("message", "")

        # Rule-based detection
        reasons = rule_based_check(text)

        # AI prediction
        ai_result = ai_predict(text)

        # Risk calculation
        risk = calculate_risk(ai_result, reasons)

        # FINAL STRICT DECISION LOGIC
        if "money" in reasons and "urgency" in reasons:
            result = "⚠️ SCAM"
        elif risk >= 60:
            result = "⚠️ SCAM"
        else:
            result = "✅ SAFE"

    return render_template(
        "index.html",
        result=result,
        risk=risk,
        reasons=reasons
    )

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
        debug=False
    )
