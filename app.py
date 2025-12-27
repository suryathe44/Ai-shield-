from flask import Flask, render_template, request
import joblib

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
def home():
    result = ""
    reason = ""

    if request.method == "POST":
        user_text = request.form["message"]
        result, reason = predict_message(user_text)

    return render_template("index.html", result=result, reason=reason)

if __name__ == "__main__":
    app.run(debug=True, port=8000)

