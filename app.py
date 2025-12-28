from flask import Flask, render_template, request
import joblib
import os

from utils.rules import rule_based_check
from utils.risk_score import calculate_risk

app = Flask(__name__)

# Load model
model = joblib.load("model/scam_model.pkl")
vectorizer = joblib.load("model/vectorizer.pkl")


def predict_message(text):
    vec = vectorizer.transform([text])
    prediction = model.predict(vec)[0]
    return prediction


@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    risk = 0
    flags = []

    if request.method == "POST":
        user_text = request.form["message"]

        flags = rule_based_check(user_text)
        ai_result = predict_message(user_text)

        risk = calculate_risk(ai_result, flags)

        if risk >= 70:
            result = "⚠️ SCAM (High Risk)"
        elif risk >= 40:
            result = "⚠️ SUSPICIOUS"
        else:
            result = "✅ SAFE"

    return render_template(
        "index.html",
        result=result,
        risk=risk,
        flags=flags
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000))
    )
