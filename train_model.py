import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Load data
data = pd.read_csv("dataset.csv")

X = data["text"]
y = data["label"]

# Vectorizer
vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)

# Model
model = LogisticRegression()
model.fit(X_vec, y)

# Save
joblib.dump(model, "model/scam_model.pkl")
joblib.dump(vectorizer, "model/vectorizer.pkl")

print("✅ Model & vectorizer saved successfully")
