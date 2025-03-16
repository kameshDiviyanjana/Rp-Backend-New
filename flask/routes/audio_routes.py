from flask import Blueprint, request, jsonify
from models.lstm_encoder import encoder_model, kmeans
from utils.audio_processing import preprocess_audio

audio_bp = Blueprint("audio_bp", __name__)

@audio_bp.route('/predict', methods=['POST'])
def predict_cluster():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Preprocess the audio file directly from memory
        audio_data = preprocess_audio(file)
        if audio_data is None:
            return jsonify({"error": "Invalid audio file"}), 400

        # Extract latent features using the encoder
        latent_features = encoder_model.predict(audio_data)

        # Predict cluster
        cluster = kmeans.predict(latent_features)[0]

        # Calculate distances to cluster centroids for confidence
        distances = kmeans.transform(latent_features)[0]
        closest_distance = distances[cluster]
        max_distance = distances.max()
        confidence = 100 * (1 - (closest_distance / max_distance))

        return jsonify({
            "cluster": int(cluster),
            "confidence": f"{confidence:.2f}%"
        })
    except Exception as e:
        print(f"Error in prediction: {e}")
        return jsonify({"error": "Error processing the file"}), 500
# def predict_cluster():
#     if 'file' not in request.files:
#         return jsonify({"error": "No file provided"}), 400

#     file = request.files['file']
#     audio_data = preprocess_audio(file)
#     if audio_data is None:
#         return jsonify({"error": "Invalid audio file"}), 400

#     latent_features = encoder_model.predict(audio_data)
#     cluster = kmeans.predict(latent_features)[0]

#     return jsonify({"cluster": int(cluster),"confidence": f"{confidence:.2f}%"})#