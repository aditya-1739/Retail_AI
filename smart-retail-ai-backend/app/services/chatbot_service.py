import json
import joblib

# Load chatbot model
model = joblib.load("app/models/chatbot_model.pkl")

# Load TF-IDF vectorizer
vectorizer = joblib.load("app/models/chatbot_vectorizer.pkl")

# Load intents
with open("app/models/intents.json", "r") as file:
    data = json.load(file)

responses = {}

for intent in data["intents"]:
    responses[intent["tag"]] = intent["responses"]


def chatbot_response(message: str):
    vector = vectorizer.transform([message])
    tag = model.predict(vector)[0]
    return {
        "response": responses[tag][0],
        "tag": tag
    }