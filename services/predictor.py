def predict_ai(text, model, vectorizer):
    vector = vectorizer.transform([text])
    prediction = model.predict(vector)[0]
    return prediction
