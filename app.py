from flask import Flask, render_template, request
import joblib
import os

app = Flask(__name__)

# Load AI model
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")


# 🔐 Rule-based scam check
def rule_based_check(text):
    red_flags = [
        "₹", "rs", "inr", "send money", "pay",
        "urgent", "account block", "bank details",
        "processing fee", "transfer money"
    ]

    count = 0
    for flag in red_flags:
        if flag in text.lower():
            count += 1

    return count >= 2


# 🤖 ML + Rule-based prediction
def predict_message(text):
    text_vec = vectorizer.transform([text])
    prediction = model.predict(text_vec)[0]

    # Rule-based override
    if rule_based_check(text):
        return "⚠️ SCAM (High Risk – Money Fraud)", "Money request + urgency detected."

    elif prediction == "scam":
        return "⚠️ SCAM", "This message matches known scam patterns."

    else:
        return "✅ SAFE", "This message appears safe, but always stay cautious."


# 🌐 Home route
@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    reason = ""

    if request.method == "POST":
        user_text = request.form["message"]
        result, reason = predict_message(user_text)

    return render_template("index.html", result=result, reason=reason)


# ▶️ Run app
if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000))
    )






