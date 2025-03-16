from flask import Blueprint, request, jsonify
from utils.image_processing import process_image
from models.hand_gesture import gesture_model
import numpy as np

image_bp = Blueprint("image_bp", __name__)

@image_bp.route("/predict-math", methods=["POST"])
def predict():
    try:
        # Check if image exists
        if "image" not in request.files:
            return jsonify({"error": "No image uploaded"}), 400

        # Read image
        image = request.files["image"].read()

        # Preprocess image
        processed_image = process_image(image)

        # Make prediction (probabilities for numbers 0-9)
        prediction_probs = gesture_model.predict(processed_image)[0]

        # Get top-2 predicted numbers
        top_2_indices = np.argsort(prediction_probs)[-2:][::-1]  # Get top 2 classes
        top_1, top_2 = top_2_indices[0], top_2_indices[1]

        # Get probabilities
        top_1_prob, top_2_prob = prediction_probs[top_1], prediction_probs[top_2]

        print(f"Top-1: {top_1} ({top_1_prob*100:.2f}%), Top-2: {top_2} ({top_2_prob*100:.2f}%)")

        # If top prediction confidence is above 80%, accept it
        if top_1_prob >= 0.80:
            final_prediction = str(top_1)
        else:
            # If second best prediction is close (within 10% of top-1), accept it
            if (top_1_prob - top_2_prob) < 0.10:
                final_prediction = str(top_2)
            else:
                final_prediction = "Unknown"

        return jsonify({"prediction": final_prediction, "confidence": f"{top_1_prob*100:.2f}%"})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": "Prediction failed"}), 500
# def predict():
#     if "image" not in request.files:
#         return jsonify({"error": "No image uploaded"}), 400

#     image = request.files["image"].read()
#     processed_image = process_image(image)
#     prediction_probs = gesture_model.predict(processed_image)[0]

#     top_1 = np.argmax(prediction_probs)
#     return jsonify({"prediction": str(top_1)})
