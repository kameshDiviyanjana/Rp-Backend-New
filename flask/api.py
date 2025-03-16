# import io
# import numpy as np
# import librosa
# from sklearn.preprocessing import MinMaxScaler
# from tensorflow.keras.models import load_model
# from sklearn.cluster import KMeans
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from werkzeug.serving import run_simple
# import tensorflow as tf
# import mediapipe as mp
# import os
# import cv2
# from PIL import Image



# # Initialize Flask app
# app = Flask(__name__)
# CORS(app)

# # Load the pre-trained LSTM encoder model
# encoder_model = load_model("lstm_encoder_model.keras")

# # Load clustering model
# clusters = np.load("clusters1.npy")  # Cluster mapping
# num_clusters = len(np.unique(clusters))
# kmeans = KMeans(n_clusters=num_clusters, random_state=42)
# latent_features = np.load("latent_features1.npy")
# kmeans.fit(latent_features)

# # Audio preprocessing functions
# def preprocess_audio(file, sr=16000, n_mfcc=13, max_timesteps=100):
#     try:
#         # Read the audio file directly from memory
#         audio, _ = librosa.load(io.BytesIO(file.read()), sr=sr)
        
#         # Extract MFCC features
#         mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=n_mfcc).T  # Corrected this line
        
#         # Pad or truncate the MFCC sequence to match the max_timesteps
#         if len(mfccs) < max_timesteps:
#             pad_width = max_timesteps - len(mfccs)
#             mfccs = np.pad(mfccs, ((0, pad_width), (0, 0)), mode='constant')
#         else:
#             mfccs = mfccs[:max_timesteps]

#         # Normalize the MFCC features
#         scaler = MinMaxScaler()
#         mfccs_normalized = scaler.fit_transform(mfccs)

#         return np.expand_dims(mfccs_normalized, axis=0)  # Add batch dimension
#     except Exception as e:
#         print(f"Error processing audio file: {e}")
#         return None

# @app.route('/predict', methods=['POST'])
# def predict_cluster():
#     if 'file' not in request.files:
#         return jsonify({"error": "No file provided"}), 400

#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({"error": "No selected file"}), 400

#     try:
#         # Preprocess the audio file directly from memory
#         audio_data = preprocess_audio(file)
#         if audio_data is None:
#             return jsonify({"error": "Invalid audio file"}), 400

#         # Extract latent features using the encoder
#         latent_features = encoder_model.predict(audio_data)

#         # Predict cluster
#         cluster = kmeans.predict(latent_features)[0]

#         # Calculate distances to cluster centroids for confidence
#         distances = kmeans.transform(latent_features)[0]
#         closest_distance = distances[cluster]
#         max_distance = distances.max()
#         confidence = 100 * (1 - (closest_distance / max_distance))

#         return jsonify({
#             "cluster": int(cluster),
#             "confidence": f"{confidence:.2f}%"
#         })
#     except Exception as e:
#         print(f"Error in prediction: {e}")
#         return jsonify({"error": "Error processing the file"}), 500



# # Load the trained model
# model_path = "./model/action_recognition_model.keras"
# model = tf.keras.models.load_model(model_path)

# # Label encoder classes
# label_encoder_classes = [
#     "catch", "dribble", "handstand", "jump", "kick_ball", "run", "somersault", "throw", "walk"
# ]

# # MediaPipe Pose Initialization
# mp_pose = mp.solutions.pose
# pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# # Helper Functions
# def extract_skeleton_from_frame(frame):
#     frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     results = pose.process(frame_rgb)
#     if results.pose_landmarks:
#         keypoints = []
#         for landmark in results.pose_landmarks.landmark:
#             keypoints.append([landmark.x, landmark.y, landmark.z])
#         return np.array(keypoints)
#     return None

# def normalize_keypoints(keypoints):
#     reference_point = keypoints[0, :2]
#     normalized = keypoints[:, :2] - reference_point
#     return normalized

# def prepare_sequence(sequence, sequence_length=30):
#     if len(sequence) >= sequence_length:
#         return sequence[:sequence_length]
#     else:
#         padding = np.zeros((sequence_length - len(sequence), sequence.shape[1]))
#         return np.vstack((sequence, padding))

# @app.route('/upload', methods=['POST'])
# def upload_video():
#     if 'file' not in request.files:
#         return jsonify({"error": "No file provided"}), 400

#     file = request.files['file']
#     input_path = f"uploads/{file.filename}"
#     output_path = f"outputs/{os.path.splitext(file.filename)[0]}_processed.mp4"

#     # Save uploaded file
#     os.makedirs("uploads", exist_ok=True)
#     os.makedirs("outputs", exist_ok=True)
#     file.save(input_path)

#     # Process video
#     cap = cv2.VideoCapture(input_path)
#     frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     fps = int(cap.get(cv2.CAP_PROP_FPS))

#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

#     sequence = []
#     sequence_length = 30
#     predictions = []

#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break

#         keypoints = extract_skeleton_from_frame(frame)
#         if keypoints is not None:
#             normalized_keypoints = normalize_keypoints(keypoints)
#             sequence.append(normalized_keypoints.flatten())

#             if len(sequence) == sequence_length:
#                 input_sequence = prepare_sequence(np.array(sequence), sequence_length=sequence_length)
#                 input_sequence = input_sequence.reshape(1, sequence_length, -1)

#                 prediction = model.predict(input_sequence)
#                 predicted_label = label_encoder_classes[np.argmax(prediction)]

#                 feedback = f"Detected action: {predicted_label}"
#                 predictions.append({"frame": len(predictions) + 1, "prediction": predicted_label, "feedback": feedback})

#                 cv2.putText(frame, f"Action: {predicted_label}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
#                 sequence.pop(0)

#         out.write(frame)

#     cap.release()
#     out.release()

#     # Send predictions and video as response
#     return jsonify({
#         "predictions": predictions,
#         "video_url": output_path
#     })


# MODEL_PATH = "./model/hand_gesture_model.h5"
# model = tf.keras.models.load_model(MODEL_PATH)

# # Preprocess image function
# def process_image(image):
#     img = Image.open(io.BytesIO(image))
#     img = img.convert("RGB")  # Convert to RGB (3-channel)
#     img = img.resize((64, 64))  # Resize to match model input
#     img_array = np.array(img) / 255.0  # Normalize pixel values
#     img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
#     return img_array  # Shape (1, 64, 64, 3)

# @app.route("/predict-math", methods=["POST"])
# def predict():
#     try:
#         # Check if image exists
#         if "image" not in request.files:
#             return jsonify({"error": "No image uploaded"}), 400

#         # Read image
#         image = request.files["image"].read()

#         # Preprocess image
#         processed_image = process_image(image)

#         # Make prediction (probabilities for numbers 0-9)
#         prediction_probs = model.predict(processed_image)[0]

#         # Get top-2 predicted numbers
#         top_2_indices = np.argsort(prediction_probs)[-2:][::-1]  # Get top 2 classes
#         top_1, top_2 = top_2_indices[0], top_2_indices[1]

#         # Get probabilities
#         top_1_prob, top_2_prob = prediction_probs[top_1], prediction_probs[top_2]

#         print(f"Top-1: {top_1} ({top_1_prob*100:.2f}%), Top-2: {top_2} ({top_2_prob*100:.2f}%)")

#         # If top prediction confidence is above 80%, accept it
#         if top_1_prob >= 0.80:
#             final_prediction = str(top_1)
#         else:
#             # If second best prediction is close (within 10% of top-1), accept it
#             if (top_1_prob - top_2_prob) < 0.10:
#                 final_prediction = str(top_2)
#             else:
#                 final_prediction = "Unknown"

#         return jsonify({"prediction": final_prediction, "confidence": f"{top_1_prob*100:.2f}%"})

#     except Exception as e:
#         print("Error:", str(e))
#         return jsonify({"error": "Prediction failed"}), 500



# # Run the Flask app
# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask
from flask_cors import CORS
from routes.audio_routes import audio_bp
from routes.video_routes import video_bp
from routes.image_routes import image_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(audio_bp, url_prefix="/audio")
app.register_blueprint(video_bp, url_prefix="/video")
app.register_blueprint(image_bp, url_prefix="/image")

if __name__ == '__main__':
    app.run(debug=True)
