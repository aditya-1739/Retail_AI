import joblib
import numpy as np
from PIL import Image

# Load trained model
model = joblib.load("app/models/face_recognition.pkl")

def recognize_face(image):

    # Convert to grayscale
    image = image.convert("L")

    # Resize to match training size
    image = image.resize((64, 64))

    # Convert to numpy
    img = np.array(image)

    # Flatten image
    img = img.reshape(1, -1)

    # Predict person ID
    person = int(model.predict(img)[0])

    # Probability (if available)
    confidence = None
    if hasattr(model, "predict_proba"):
        confidence = float(np.max(model.predict_proba(img)) * 100)

    return {
        "person_id": person,
        "confidence": round(confidence, 2) if confidence is not None else None
    }