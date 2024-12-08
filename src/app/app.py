from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.models import load_model
import numpy as np
import cv2
import os
import random

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for frontend-backend communication
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# Load the trained CNN model
# "../models/hand_gesture_model.h5"
MODEL_PATH = '../models/hand_gesture_model.h5'
model = load_model(MODEL_PATH)

# Classes for gestures
classes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'unknown']

# Endpoint to predict gestures from an uploaded image
@app.route('/predict', methods=['POST'])
def predict():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image uploaded'}), 400

        # Save the uploaded image temporarily
        file = request.files['image']
        img_path = os.path.join('temp', file.filename)
        file.save(img_path)

        # Preprocess the image
        img = cv2.imread(img_path)
        img = cv2.resize(img, (128, 128))  # Resize to match model input
        img = img / 255.0  # Normalize pixel values
        img = np.expand_dims(img, axis=0)  # Add batch dimension

        # Predict gesture
        predictions = model.predict(img)
        predicted_class = classes[np.argmax(predictions)]
        confidence = np.max(predictions)

        # Remove the temporary file
        os.remove(img_path)

        # Return prediction result
        return jsonify({'class': predicted_class, 'confidence': float(confidence)})

    except Exception as e:
        print(f"Error in /predict endpoint: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500


# Endpoint to generate a math problem
@app.route('/generate-problem', methods=['GET'])
def generate_problem():
    try:
        num1 = random.randint(0, 5)
        if random.choice(['+', '-']) == '-':
            num2 = random.randint(0, num1)  # Ensure num2 is <= num1 to avoid negative results
            operation = '-'
        else:
            num2 = random.randint(0, 5)
            operation = '+'

        # Calculate the correct answer
        correct_answer = num1 + num2 if operation == '+' else num1 - num2

        # Log the generated problem and answer
        print(f"Generated Problem: {num1} {operation} {num2}, Correct Answer: {correct_answer}")

        # Return the problem and correct answer
        return jsonify({'problem': f"{num1} {operation} {num2}", 'correct_answer': correct_answer})

    except Exception as e:
        print(f"Error in /generate-problem endpoint: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500


# Endpoint to solve the math problem with gestures
@app.route('/math-practice', methods=['POST'])
def math_practice():
    try:
        # Parse problem and correct answer from the request
        problem = request.form.get('problem')
        correct_answer = int(request.form.get('correct_answer'))

        # Check if an image is uploaded
        if 'image' not in request.files:
            return jsonify({'error': 'No image uploaded'}), 400

        # Save and preprocess the image
        file = request.files['image']
        img_path = os.path.join('temp', file.filename)
        file.save(img_path)

        img = cv2.imread(img_path)
        img = cv2.resize(img, (128, 128))
        img = img / 255.0
        img = np.expand_dims(img, axis=0)

        # Predict the gesture
        predictions = model.predict(img)
        predicted_class_index = np.argmax(predictions)
        predicted_class = classes[predicted_class_index]  # Get class label
        confidence = predictions[0][predicted_class_index]  # Get confidence score

        # Clean up temporary file
        os.remove(img_path)

        # Handle the 'unknown' prediction case
        if predicted_class == 'unknown':
            feedback = "Prediction uncertain. Please try again with a clearer hand gesture."
            print(f"Problem: {problem}, Correct Answer: {correct_answer}, Predicted Class: {predicted_class}, Feedback: {feedback}")
            return jsonify({
                'feedback': feedback,
                'predicted_class': predicted_class,
                'confidence': float(confidence),
                'correct_answer': correct_answer
            })

        # Convert predicted class to an integer and compare with the correct answer
        predicted_class = int(predicted_class)
        is_correct = (predicted_class == correct_answer)
        feedback = "Correct!" if is_correct else f"Incorrect. The correct answer is {correct_answer}."

        # Log details for debugging
        print(f"Problem: {problem}, Correct Answer: {correct_answer}, Predicted Class: {predicted_class}, Feedback: {feedback}")

        # Return the feedback and predicted class
        return jsonify({
            'feedback': feedback,
            'predicted_class': predicted_class,
            'confidence': float(confidence),
            'correct_answer': correct_answer
        })

    except Exception as e:
        print(f"Error in /math-practice endpoint: {e}")
        return jsonify({'error': 'Internal Server Error', 'message': str(e)}), 500


# Endpoint to detect gestures in real-time video
@app.route('/realtime', methods=['GET'])
def realtime():
    try:
        def generate_frames():
            cap = cv2.VideoCapture(0)  # Access the webcam
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                # Preprocess frame
                resized_frame = cv2.resize(frame, (128, 128))
                normalized_frame = resized_frame / 255.0
                normalized_frame = np.expand_dims(normalized_frame, axis=0)

                # Predict gesture
                predictions = model.predict(normalized_frame)
                predicted_class = classes[np.argmax(predictions)]

                # Add prediction to frame
                cv2.putText(frame, f"Gesture: {predicted_class}", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                # Convert frame to bytes
                _, buffer = cv2.imencode('.jpg', frame)
                frame_bytes = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        return generate_frames()
    except Exception as e:
        print(f"Error in /realtime endpoint: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500


if __name__ == '__main__':
    os.makedirs('temp', exist_ok=True)
    app.run(debug=True, port=5000)
