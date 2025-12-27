from flask import Flask, render_template, request
import joblib
import os 
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
app = Flask(__name__)
# Load AI model
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

def predict_message(text):
    text_vec = vectorizer.transform([text])
    prediction = model.predict(text_vec)[0]

    if prediction == "scam":
        return "SCAM", "This message looks like a scam based on learned patterns."
    else:
        return "SAFE", "This message appears safe, but always stay cautious."

@app.route("/", methods=["GET", "POST"])
if rule_based_check(user_text):
    result = "⚠️ SCAM (High Risk – Money Fraud)"
elif prediction == "scam":
    result = "⚠️ SCAM"
else:
    result = "✅ SAFE"

def home():
    result = ""
    reason = ""

    if request.method == "POST":
        user_text = request.form["message"]
        result, reason = predict_message(user_text)

    return render_template("index.html", result=result, reason=reason)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))




