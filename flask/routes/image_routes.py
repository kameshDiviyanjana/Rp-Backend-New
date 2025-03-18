from flask import Blueprint, request, jsonify
import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
import os
import traceback
from utils.image_processing import process_image
from models.hand_gesture import gesture_model

image_bp = Blueprint("image_bp", __name__)


# Load Model
# Change the path reference to be more robust
model_path = os.path.join(os.path.dirname(__file__), "..", "model", "hand_gesture_model.h5")

if not os.path.exists(model_path):
    print(f"❌ Model file not found at {model_path}")
    model = None
else:
    try:
        model = tf.keras.models.load_model(model_path, compile=False)
        print("✅ Model loaded successfully")
    except Exception as e:
        print("❌ Error loading model:", str(e))
        traceback.print_exc()
        model = None  # Avoid breaking the app


try:
    model = tf.keras.models.load_model(model_path, compile=False)
    print("✅ Model loaded successfully")
except Exception as e:
    print("❌ Error loading model:", str(e))
    traceback.print_exc()

## Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.6)

# Gesture class labels
class_labels = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

def process_frame(image):
    rgb_frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        h, w, _ = image.shape

        x_min = min([int(l.x * w) for l in hand_landmarks.landmark])
        y_min = min([int(l.y * h) for l in hand_landmarks.landmark])
        x_max = max([int(l.x * w) for l in hand_landmarks.landmark])
        y_max = max([int(l.y * h) for l in hand_landmarks.landmark])

        # Expand bounding box slightly
        x_min, y_min = max(0, x_min - 20), max(0, y_min - 20)
        x_max, y_max = min(w, x_max + 20), min(h, y_max + 20)

        hand_region = image[y_min:y_max, x_min:x_max]

        if hand_region.size == 0:
            return None  # Skip if no valid region

        hand_region = cv2.resize(hand_region, (64, 64))
        hand_region = np.expand_dims(hand_region, axis=0) / 255.0

        prediction = model.predict(hand_region)
        class_index = np.argmax(prediction)
        return class_labels[class_index]  # Ensuring correct variable name

    return None

@image_bp.route("/predict-math", methods=["POST"])
def predict():
    try:
        if "image" not in request.files:
            print("❌ No image file received")
            return jsonify({"error": "No image uploaded"}), 400

        file = request.files["image"]
        print(f"✅ Received image: {file.filename}")

        # Convert file to numpy array
        file_bytes = np.frombuffer(file.read(), np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        if image is None:
            print("❌ Could not decode image")
            return jsonify({"error": "Invalid image format"}), 400

        # Debugging: Check image shape
        print(f"🔍 Image shape: {image.shape}")

        prediction = process_frame(image)
        if prediction:
            print(f"✅ Prediction: {prediction}")
            return jsonify({"prediction": prediction})
        else:
            print("❌ No hand detected")
            return jsonify({"error": "No hand detected"}), 400

    except Exception as e:
        print("❌ Flask error:", str(e))
        traceback.print_exc()
        return jsonify({"error": "Internal server error", "details": str(e)}), 500
