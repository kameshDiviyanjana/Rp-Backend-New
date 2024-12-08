from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from tensorflow.keras.models import load_model
import numpy as np
import cv2
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the trained model
MODEL_PATH = '../models/hand_gesture_model.h5'
model = load_model(MODEL_PATH)

# Classes
classes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'unknown']

# Define the prediction endpoint
@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']
    img_path = os.path.join('temp', file.filename)
    file.save(img_path)

    img = cv2.imread(img_path)
    img = cv2.resize(img, (128, 128))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    predictions = model.predict(img)
    predicted_class = classes[np.argmax(predictions)]
    confidence = np.max(predictions)

    os.remove(img_path)

    return jsonify({'class': predicted_class, 'confidence': float(confidence)})

if __name__ == '__main__':
    os.makedirs('temp', exist_ok=True)
    app.run(debug=True, port=5000)
