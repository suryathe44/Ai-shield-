from flask import Flask, render_template, request
import joblib
import os

from utils.rules import rule_based_check
from utils.risk_score import calculate_risk

app = Flask(__name__)

# ---------- SAFE MODEL LOADING ----------
model = None
vectorizer = None

try:
    model = joblib.load("model/scam_model.pkl")
    vectorizer = joblib.load("model/vectorizer.pkl")
    print("✅ Model loaded successfully")
except Exception as e:
    print("⚠️ Model load failed, running in rule-based mode only")
    print(e)

# ---------- AI PREDICTION ----------
def ai_predict(text):
    if model is None or vectorizer is None:
        return "unknown"
    vec = vectorizer.transform([text])
    return model.predict(vec)[0]

# ---------- ROUTE ----------
@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    risk = 0
    reasons = []

    if request.method == "POST":
        text = request.form["message"]

        reasons = rule_based_check(text)
        ai_result = ai_predict(text)
        risk = calculate_risk(ai_result, reasons)
# FINAL DECISION LOGIC
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

# ---------- RUN ----------
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000))
    )


