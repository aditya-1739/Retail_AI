import joblib

# Load model and vectorizer
model = joblib.load("app/models/sentiment_model.pkl")
vectorizer = joblib.load("app/models/vectorizer.pkl")

def analyze_sentiment(review: str):
    review_vector = vectorizer.transform([review])
    prediction = model.predict(review_vector)[0]

    sentiment = "Positive" if prediction == 1 else "Negative"

    return {
        "review": review,
        "sentiment": sentiment
    }