import numpy as np
import tensorflow as tf
from PIL import Image

# Load the trained model
model = tf.keras.models.load_model("app/models/product_classifier.h5")

# Fashion-MNIST class names
class_names = [
    "T-shirt",
    "Trouser",
    "Pullover",
    "Dress",
    "Coat",
    "Sandal",
    "Shirt",
    "Sneaker",
    "Bag",
    "Ankle boot"
]

def predict_product(image):
    # Convert to grayscale
    image = image.convert("L")

    # Resize to 96x96 (same size used during training)
    image = image.resize((96, 96))

    # Convert to NumPy
    img = np.array(image)

    # Normalize
    img = img / 255.0

    # Convert grayscale to RGB
    img = np.stack((img,) * 3, axis=-1)

    # Add batch dimension
    img = np.expand_dims(img, axis=0)

    # Predict
    prediction = model.predict(img, verbose=0)

    class_index = np.argmax(prediction)

    confidence = float(np.max(prediction) * 100)

    return {
        "category": class_names[class_index],
        "confidence": round(confidence, 2)
    }