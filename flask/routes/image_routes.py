from flask import Blueprint, request, jsonify
import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
import os
import traceback

image_bp = Blueprint("image_bp", __name__)

# Load Model
model_path = os.path.join(os.path.dirname(__file__), "..", "model", "hand_gesture_model.h5")
model = None
if os.path.exists(model_path):
    try:
        model = tf.keras.models.load_model(model_path, compile=False)
        print("✅ Model loaded successfully")
    except Exception as e:
        print(f"❌ Error loading model: {str(e)}")
        traceback.print_exc()
else:
    print(f"❌ Model file not found at {model_path}")

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=1,
    min_detection_confidence=0.7
)

# Class labels (0-5 for your use case)
class_labels = ['0', '1', '2', '3', '4', '5']

def preprocess_image(image):
    """Enhance image quality before hand detection."""
    rgb_frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    alpha = 1.3  # Slightly higher contrast
    beta = 15    # Slightly higher brightness
    enhanced_frame = cv2.convertScaleAbs(rgb_frame, alpha=alpha, beta=beta)
    return enhanced_frame

def is_finger_extended(tip_y, pip_y, mcp_y):
    """Determine if a finger is extended based on landmark positions."""
    # Finger is extended if tip is above PIP and MCP joints (y decreases upward in image coordinates)
    return tip_y < pip_y and tip_y < mcp_y

def analyze_hand_skeleton(landmarks, h, w):
    """Analyze hand skeleton to determine gesture based on finger states."""
    # Convert landmarks to pixel coordinates
    lm = [(int(l.x * w), int(l.y * h)) for l in landmarks.landmark]

    # Landmark indices (MediaPipe hand landmarks):
    # Thumb: 4 (tip), 3 (IP), 2 (MCP)
    # Index: 8 (tip), 6 (PIP), 5 (MCP)
    # Middle: 12 (tip), 10 (PIP), 9 (MCP)
    # Ring: 16 (tip), 14 (PIP), 13 (MCP)
    # Pinky: 20 (tip), 18 (PIP), 17 (MCP)

    # Check finger states (only y-coordinate matters for extension)
    fingers = {
        "thumb": is_finger_extended(lm[4][1], lm[3][1], lm[2][1]),
        "index": is_finger_extended(lm[8][1], lm[6][1], lm[5][1]),
        "middle": is_finger_extended(lm[12][1], lm[10][1], lm[9][1]),
        "ring": is_finger_extended(lm[16][1], lm[14][1], lm[13][1]),
        "pinky": is_finger_extended(lm[20][1], lm[18][1], lm[17][1])
    }

    # Count extended fingers (excluding thumb for simplicity, as "5" typically focuses on 4 fingers + thumb)
    extended_fingers = sum([fingers["index"], fingers["middle"], fingers["ring"], fingers["pinky"]])

    # Skeleton-based gesture logic
    if extended_fingers == 0 and fingers["thumb"]:  # Thumb up only
        return "1"
    elif extended_fingers == 1 and fingers["index"]:  # Index only
        return "1"
    elif extended_fingers == 2 and fingers["index"] and fingers["middle"]:  # Index + Middle
        return "2"
    elif extended_fingers == 3 and fingers["index"] and fingers["middle"] and fingers["ring"]:  # Index + Middle + Ring
        return "3"
    elif extended_fingers == 4 and fingers["index"] and fingers["middle"] and fingers["ring"] and fingers["pinky"]:  # All four
        return "4" if not fingers["thumb"] else "5"  # "5" if thumb is also extended
    elif extended_fingers == 0 and not any(fingers.values()):  # Fist
        return "0"
    return None  # Unknown gesture

def process_frame(image):
    """Process image and predict gesture using hybrid CNN + skeleton logic."""
    rgb_frame = preprocess_image(image)
    results = hands.process(rgb_frame)

    if not results.multi_hand_landmarks:
        print("❌ No hand detected")
        return None, 0.0

    hand_landmarks = results.multi_hand_landmarks[0]
    h, w, _ = image.shape

    # Skeleton-based prediction
    skeleton_pred = analyze_hand_skeleton(hand_landmarks, h, w)
    print(f"🔍 Skeleton prediction: {skeleton_pred}")

    # CNN-based prediction
    # Calculate bounding box with more padding for context
    x_min = max(0, min([int(l.x * w) for l in hand_landmarks.landmark]) - 40)
    y_min = max(0, min([int(l.y * h) for l in hand_landmarks.landmark]) - 40)
    x_max = min(w, max([int(l.x * w) for l in hand_landmarks.landmark]) + 40)
    y_max = min(h, max([int(l.y * h) for l in hand_landmarks.landmark]) + 40)

    if x_max <= x_min or y_max <= y_min:
        print("❌ Invalid bounding box")
        return skeleton_pred, 0.7 if skeleton_pred else 0.0  # Fallback to skeleton with moderate confidence

    hand_region = image[y_min:y_max, x_max:x_min]
    if hand_region.size == 0:
        print("❌ Empty hand region")
        return skeleton_pred, 0.7 if skeleton_pred else 0.0

    try:
        hand_region = cv2.resize(hand_region, (64, 64), interpolation=cv2.INTER_AREA)
    except Exception as e:
        print(f"❌ Resize error: {str(e)}")
        return skeleton_pred, 0.7 if skeleton_pred else 0.0

    # Normalize and predict with CNN
    hand_region = hand_region.astype(np.float32) / 255.0
    hand_region = np.expand_dims(hand_region, axis=0)

    if model is None:
        print("❌ Model not available")
        return skeleton_pred, 0.7 if skeleton_pred else 0.0

    try:
        prediction = model.predict(hand_region, verbose=0)
        class_index = np.argmax(prediction)
        confidence = float(prediction[0][class_index])
        cnn_pred = class_labels[class_index]
        print(f"🔍 CNN prediction: {cnn_pred} with confidence {confidence:.2f}")

        # Hybrid logic: Use CNN if confident, otherwise fallback to skeleton
        if confidence >= 0.85:  # High confidence threshold
            final_pred = cnn_pred
            final_conf = confidence
        elif skeleton_pred and confidence < 0.6:  # CNN is unsure, skeleton is confident
            final_pred = skeleton_pred
            final_conf = 0.7  # Assign moderate confidence to skeleton
        else:
            final_pred = cnn_pred if confidence > 0.6 else skeleton_pred
            final_conf = confidence if confidence > 0.6 else (0.7 if skeleton_pred else 0.0)

        return final_pred, final_conf
    except Exception as e:
        print(f"❌ Prediction error: {str(e)}")
        return skeleton_pred, 0.7 if skeleton_pred else 0.0

@image_bp.route("/predict-math", methods=["POST"])
def predict():
    try:
        if "image" not in request.files:
            print("❌ No image file received")
            return jsonify({"error": "No image uploaded"}), 400

        file = request.files["image"]
        print(f"✅ Received image: {file.filename}")

        file_bytes = np.frombuffer(file.read(), np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        if image is None:
            print("❌ Could not decode image")
            return jsonify({"error": "Invalid image format"}), 400

        print(f"🔍 Image shape: {image.shape}")
        prediction, confidence = process_frame(image)
        if prediction:
            return jsonify({"prediction": prediction, "confidence": confidence})
        else:
            return jsonify({"error": "No hand detected or prediction failed"}), 400

    except Exception as e:
        print(f"❌ Flask error: {str(e)}")
        traceback.print_exc()
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

def shutdown():
    hands.close()
    print("✅ MediaPipe Hands closed")

import atexit
atexit.register(shutdown)