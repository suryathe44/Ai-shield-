from flask import Flask, render_template, request
import joblib
import os

from utils.rules import rule_based_check
from utils.risk_score import calculate_risk
from utils.language import detect_language
from services.predictor import predict_ai

app = Flask(__name__)

model = joblib.load("model/scam_model.pkl")
vectorizer = joblib.load("model/vectorizer.pkl")

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    reasons = []
    risk = 0

    if request.method == "POST":
        text = request.form["message"]
        lang = detect_language(text)

        ai_result = predict_ai(text, model, vectorizer)
        rule_flags = rule_based_check(text)
        risk = calculate_risk(ai_result, rule_flags)

        if risk >= 70:
            result = "⚠️ SCAM"
        else:
            result = "✅ SAFE"

        reasons = rule_flags

    return render_template("index.html",
                           result=result,
                           risk=risk,
                           reasons=reasons)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))








